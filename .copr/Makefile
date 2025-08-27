pkgs:
	dnf -y install fedpkg rpmdevtools rpmautospec

sources: pkgs
	spectool --gf cie-middleware.spec

srpm: sources
	git config --global --add safe.directory .
	fedpkg --release f40 srpm
	cp *.src.rpm $(outdir)
