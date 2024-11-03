Name:			cie-middleware
Version:		1.4.3.9
Release:		%autorelease
Summary:		Middleware for CIE (Italian Electronic ID Card)
License:		BSD-3-Clause
URL:			https://github.com/italia/cie-middleware-linux

ExclusiveArch:	%{java_arches}

Source0:		https://github.com/italia/cie-middleware-linux/archive/%{version}/%{name}-linux-%{version}.tar.gz
Source1:		CMakeLists.txt
Source2:		cieid.desktop
Source3:		pom.xml
Source4:		libcie-pkcs11.module

Patch1:			cie-middleware-common-fixup.patch
Patch2:			cie-middleware-cie-pkcs11-fixup.patch
Patch3:			cie-middleware-fix-pades.patch
Patch4:			cie-middleware-fix-cryptopp.patch
Patch5:			cie-middleware-merge-fix.patch
Patch6:			cie-middleware-fix-pkcs11.patch
Patch7:			cie-middleware-fix-openssl.patch
Patch8:			cie-middleware-fix-c++-std-headers.patch
Patch9:			cie-middleware-keyboard-shortcuts.patch
Patch10:			cie-middleware-fix-pkcs11-info-output.patch
Patch11:			cie-middleware-fix-pkcs11-cant-lock.patch
Patch12:			cie-middleware-fix-chromium-buffer-overflow.patch
Patch13:			cie-middleware-override-tutorial.patch
Patch14:			cie-middleware-reduce-verbosity.patch
Patch15:			cie-middleware-improve-graphical-signature.patch
Patch16:			cie-middleware-fix-deallocation-mismatch.patch
Patch17:			cie-middleware-generate-transparent-signature.patch
Patch18:			cie-middleware-ignore-unrecognised-tokens.patch
Patch19:			cie-middleware-FirmaConCIE-fix-error-path.patch
Patch20:			cie-middleware-FirmaConCIE-make-progress-more-uniform.patch
Patch21:			cie-middleware-cieid-make-window-resizable.patch
Patch22:			cie-middleware-PINManager-fix-error-path.patch
Patch23:			cie-middleware-AbilitaCIE-fix-error-path.patch
Patch24:			cie-middleware-cieid-jframe-set-icon-and-title.patch

%if 0%{?fedora} < 40 || (0%{?rhel} && 0%{?rhel} < 10)
BuildRequires:  maven-local-openjdk11
%else
BuildRequires:  maven-local
%endif
BuildRequires:	cmake
BuildRequires:	git
BuildRequires:	gcc-c++
BuildRequires:	libcurl-devel
BuildRequires:	bzip2-devel
BuildRequires:	cryptopp-devel
BuildRequires:	freetype-devel
BuildRequires:	glibc
BuildRequires:	libpng-devel
BuildRequires:	libxml2-devel
BuildRequires:	openssl-devel
%if 0%{?fedora} >= 41
BuildRequires:	openssl-devel-engine
%endif
BuildRequires:	zlib-devel
BuildRequires:	fontconfig-devel
BuildRequires:	pcsc-lite-devel
BuildRequires:	podofo-devel

BuildRequires:	mvn(com.google.code.gson:gson)
BuildRequires:	mvn(net.java.dev.jna:jna)
BuildRequires:	mvn(org.ghost4j:ghost4j)
BuildRequires:	mvn(ch.swingfx:twinkle)

Requires:		xmvn-tools
Requires:		dejavu-sans-fonts

%description
Middleware for CIE (Carta di Identità Elettronica).
A Java app to sign and verify documents and to manage the card.
A PKCS11 library to allow programs to use the card.

%{?javadoc_package}

%prep
%autosetup -n %{name}-linux-%{version} -p1

# Remove pre-compiled static libs
rm -rf cie_sign_sdk/Dependencies

# Remove cryptopp headers
rm -rf cie_sign_sdk/src/cryptopp
rm -rf cie-pkcs11/Cryptopp

# Merge cie_sign_sdk source with cie-pkcs11 source
mkdir -p libcie
rm -f cie_sign_sdk/CMakeLists.txt
rm -f cie_sign_sdk/README.mk
rm -f cie_sign_sdk/src/Util/UUC*
cp -r cie_sign_sdk/* libcie/
cp cie-pkcs11/keys.h libcie/include/
rm -f cie-pkcs11/keys.h
rm -f cie-pkcs11/*.a
rm -f cie-pkcs11/Util/funccallinfo.cpp
cp -f cie-pkcs11/Util/UUCStringTable.cpp libcie/src/
cp -f cie-pkcs11/Util/UUCStringTable.h libcie/include/
cp -f cie-pkcs11/Util/UUCHashtable.hpp libcie/include/
rm -f cie-pkcs11/Util/UUC*
cp -rf cie-pkcs11/* libcie/src/
rm -f libcie/src/Sign/definitions.h

# Add our CMakeLists.txt for libcie-pkcs11
install %{SOURCE1} CMakeLists.txt

# Cryptopp pkg-config changed from cryptopp.pc to libcryptopp.pc since f39
%if 0%{?fedora} > 38 || 0%{?rhel} > 9
sed -i '0,/cryptopp/s/cryptopp/libcryptopp/' CMakeLists.txt
%endif

# Install CIEID pom.xml file
install %{SOURCE3} pom.xml

# Remove jar artifacts
rm -rf CIEID/lib

# Set alternative names
%mvn_file :cieid cieid/cieid cieid

%build
# Build library
%cmake
%cmake_build

# Build CIEID
%mvn_build

%install
# Install library
%cmake_install

# Install CIEID
%mvn_install

# Generate wrapper script for CIEID
%global jopts -Xms1G -Xmx1G -Dawt.useSystemAAFontSettings=on
%global cpaths cieid:google-gson:jna:ghost4j:swingfx-twinkle:apache-commons-io:openpdf:slf4j
%jpackage_script it.ipzs.cieid.MainApplication "" "%{quote:%jopts}" %cpaths cieid true

# Install desktop configuration
mkdir -p %{buildroot}%{_datadir}/pixmaps
install -m 0644 CIEID/src/it/ipzs/cieid/res/logo_circle.png %{buildroot}%{_datadir}/pixmaps/cieid.png

mkdir -p %{buildroot}%{_datadir}/applications
install -m 0644 %{SOURCE2} %{buildroot}%{_datadir}/applications/cieid.desktop

# Create pkcs11 module link
mkdir -p %{buildroot}%{_libdir}/pkcs11
ln -s ../libcie-pkcs11.so %{buildroot}%{_libdir}/pkcs11/libcie-pkcs11.so

# Install module configuration for p11-kit
mkdir -p %{buildroot}%{_datadir}/p11-kit/modules
install -m 0644 %{SOURCE4} %{buildroot}%{_datadir}/p11-kit/modules/libcie-pkcs11.module

%files -f .mfiles
%license LICENSE
%{_bindir}/cieid
%{_libdir}/libcie-pkcs11.so
%{_datadir}/pixmaps/cieid.png
%{_datadir}/applications/cieid.desktop
%{_libdir}/pkcs11/libcie-pkcs11.so
%{_datadir}/p11-kit/modules/libcie-pkcs11.module

%changelog
%autochangelog
