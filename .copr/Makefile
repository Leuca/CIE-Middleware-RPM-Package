pkgs:
	dnf -y install fedpkg rpmdevtools

sources: pkgs
	curl -O $(spectool -S cie-middleware.spec 2>/dev/null | grep Source0 | cut -d" " -f 2)
	curl -O $(spectool -S cie-middleware.spec 2>/dev/null | grep Source4 | cut -d" " -f 2)

srpm: sources
	fedpkg srpm
