Name:			cie-middleware
Version:		1.4.3.9
Release:		%autorelease
Summary:		Middleware for CIE (Italian Electronic ID Card)
License:		BSD 3-Clause
URL:			https://github.com/italia/cie-middleware-linux

ExclusiveArch:	%{java_arches}

Source0:		https://github.com/italia/cie-middleware-linux/archive/%{version}/%{name}-linux-%{version}.tar.gz
Source1:		CMakeLists.txt
Source2:		logo.png
Source3:		cieid.desktop
Source4:		cieid.sh

Patch1:			cie-middleware-common-fixup.patch
Patch2:			cie-middleware-cie-pkcs11-fixup.patch
Patch3:			cie-middleware-fix-podofo.patch
Patch4:			cie-middleware-fix-cryptopp.patch
Patch5:			cie-middleware-merge-fix.patch
Patch6:			cie-middleware-fix-pkcs11.patch
Patch7:			cie-middleware-fix-openssl.patch

BuildRequires:	cmake
BuildRequires:	ant
BuildRequires:	gcc-c++
BuildRequires:	java-devel
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
BuildRequires:	podofo-devel
BuildRequires:	zlib-devel
BuildRequires:	fontconfig-devel
BuildRequires:	pcsc-lite-devel

Requires:		java

%description
Middleware for CIE (Carta di Identità Elettronica).
A Java app to sign and verify documents and to manage the card.
A PKCS11 library to allow programs to use the card.

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
sed -i 's/cryptopp/libcryptopp/g' CMakeLists.txt
%endif

%build
# Build library
%cmake
%cmake_build

# Build CIEID
pushd CIEID
	ant deploy
popd

%install
%cmake_install

mkdir -p %{buildroot}%{_javadir}/CIEID/lib
pushd CIEID
	install dist/CIEID.jar %{buildroot}%{_javadir}/CIEID/
	cp lib/*.jar %{buildroot}%{_javadir}/CIEID/lib
popd

mkdir -p %{buildroot}%{_datadir}/pixmaps
install -m 0644 %{SOURCE2} %{buildroot}%{_datadir}/pixmaps/cieid.png

mkdir -p %{buildroot}%{_datadir}/applications
install -m 0644 %{SOURCE3} %{buildroot}%{_datadir}/applications/cieid.desktop

mkdir -p %{buildroot}%{_bindir}
install -m 0755 %{SOURCE4} %{buildroot}%{_bindir}/cieid

# Remove duplicate java library
rm -f %{buildroot}%{_javadir}/CIEID/lib/jna-4.1.0.jar

# Generate classpaths
CLASSPATHS=""
for jarfile in $(ls %{buildroot}%{_javadir}/CIEID/lib);
do
	CLASSPATHS="$CLASSPATHS:/usr/share/java/CIEID/lib/$jarfile"	
done

sed -i "s!PATH!$CLASSPATHS!" %{buildroot}%{_bindir}/cieid

%check
cd CIEID
ant test

%files
%license LICENSE
%{_bindir}/cieid
%{_libdir}/libcie-pkcs11.so
%{_javadir}/CIEID/lib/*.jar
%{_javadir}/CIEID/CIEID.jar
%{_datadir}/pixmaps/cieid.png
%{_datadir}/applications/cieid.desktop

%changelog
%autochangelog
