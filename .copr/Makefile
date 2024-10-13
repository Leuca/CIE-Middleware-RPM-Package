pkgs:
	dnf -y install fedpkg rpmdevtools wget

sources: pkgs
	wget $$(spectool -S cie-middleware.spec 2>/dev/null | grep Source0 | cut -d" " -f 2)
	wget $$(spectool -S cie-middleware.spec 2>/dev/null | grep Source4 | cut -d" " -f 2)

srpm: sources
	fedpkg --release f40 srpm
	cp *.src.rpm $(outdir)
