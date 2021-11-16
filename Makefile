CFLAGS = -Weverything -fsanitize=address,undefined -fno-sanitize-recover=all

BUILDDIR = build

.SILENT:

$(BUILDDIR)/main: $(BUILDDIR)/main.o $(BUILDDIR)/shanote.o
	mkdir -p $(dir $@)
	clang $(CFLAGS) $^ -lcurl -o $@
	python elf-note-parse.py $@ .note.gitsha

$(BUILDDIR)/%.o: %.c
	mkdir -p $(dir $@)
	clang $(CFLAGS) -c $< -o $@

SHA_STALE=$(shell bash -c 'if ! diff -q <(git rev-parse HEAD) $(BUILDDIR)/sha.note > /dev/null 2>&1; then echo SHA_STALE; fi')

.PHONY: $(SHA_STALE)
$(BUILDDIR)/shanote: $(SHA_STALE)
	mkdir -p $(dir $@)
	cp shanote.prefix shanote.new
	git rev-parse HEAD | tee $(BUILDDIR)/sha.note | tr -d "\n" >> shanote.new
	mv shanote.new $@

$(BUILDDIR)/shanote.o: $(BUILDDIR)/shanote
	mkdir -p $(dir $@)
	objcopy --input binary \
		--output elf64-x86-64 \
		--binary-architecture i386:x86-64 \
		--rename-section .data=.note.gitsha \
		$^ $@

