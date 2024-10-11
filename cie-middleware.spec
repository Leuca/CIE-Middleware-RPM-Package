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
Source4:		https://github.com/podofo/podofo/archive/0.9.6/podofo-0.9.6.tar.gz
Source5:		pom.xml

Patch1:			cie-middleware-common-fixup.patch
Patch2:			cie-middleware-cie-pkcs11-fixup.patch
Patch3:			cie-middleware-fix-podofo.patch
Patch4:			cie-middleware-fix-cryptopp.patch
Patch5:			cie-middleware-merge-fix.patch
Patch6:			cie-middleware-fix-pkcs11.patch
Patch7:			cie-middleware-fix-openssl.patch
Patch8:			cie-middleware-fix-c++-std-headers.patch

%if 0%{?fedora} < 40 || (0%{?rhel} && 0%{?rhel} < 10)
BuildRequires:  maven-local-openjdk11
%else
BuildRequires:  maven-local
%endif
BuildRequires:	cmake
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

BuildRequires:	mvn(com.google.code.gson:gson)
BuildRequires:	mvn(net.java.dev.jna:jna)
BuildRequires:	mvn(org.ghost4j:ghost4j)
BuildRequires:	mvn(ch.swingfx:twinkle)

# Bundle PoDoFo to avoid fixing code where the available version is 10+
# License: LGPL 2.0
Provides:		bundled(podofo) = 0.9.6

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

# Unpack podofo
tar xvf %{SOURCE4}
mv podofo-0.9.6 podofo

# Add our CMakeLists.txt for libcie-pkcs11
install %{SOURCE1} CMakeLists.txt

# Cryptopp pkg-config changed from cryptopp.pc to libcryptopp.pc since f39
%if 0%{?fedora} > 38 || 0%{?rhel} > 9
sed -i '0,/cryptopp/s/cryptopp/libcryptopp/' CMakeLists.txt
%endif

# Install CIEID pom.xml file
install %{SOURCE5} pom.xml

# Remove jar artifacts
rm -rf CIEID/lib

# Set alternative names
%mvn_file :cieid cieid/cieid

%build
# Build and fake-install PoDoFo
export CXXFLAGS="%{optflags}"
export LDFLAGS="%{build_ldflags}"
%__cmake \
		-S podofo \
		-B podofo_build \
		-DCMAKE_BUILD_TYPE=RelWithDebInfo \
		-DPODOFO_BUILD_LIB_ONLY:BOOL=TRUE \
		-DPODOFO_BUILD_STATIC:BOOL=TRUE \
		-DCMAKE_CXX_FLAGS_RELEASE:STRING="-DNDEBUG" \
		-DCMAKE_VERBOSE_MAKEFILE:BOOL=ON \
		-DCMAKE_INSTALL_DO_STRIP:BOOL=OFF \
		-DCMAKE_INSTALL_PREFIX:PATH=/ \
		-DINCLUDE_INSTALL_DIR:PATH=/include	\
		-DLIB_INSTALL_DIR:PATH=/
%__cmake --build "podofo_build" -j$(nproc) --verbose
mkdir podofo_lib
DESTDIR=./podofo_lib %__cmake --install podofo_build

# Build library
%cmake
%cmake_build

# Build CIEID
%mvn_build

%install
%cmake_install

%mvn_install

# Generate wrapper script
%jpackage_script it.ipzs.cieid.MainApplication "" OPTS CPATH cieid true

# Workaround to avoid spaces from messing up
sed -i 's/OPTS/\"-Xms1G -Xmx1G\"/' %{buildroot}%{_bindir}/cieid

# Workaround to provide classpaths with groupId:artifactId
sed -i 's/CPATH/it.ipzs:cieid com.google.code.gson:gson net.java.dev.jna:jna org.ghost4j:ghost4j ch.swingfx:twinkle apache-commons-io openpdf slf4j/' %{buildroot}%{_bindir}/cieid

mkdir -p %{buildroot}%{_datadir}/pixmaps
install -m 0644 %{SOURCE2} %{buildroot}%{_datadir}/pixmaps/cieid.png

mkdir -p %{buildroot}%{_datadir}/applications
install -m 0644 %{SOURCE3} %{buildroot}%{_datadir}/applications/cieid.desktop

%files -f .mfiles
%license LICENSE
%{_bindir}/cieid
%{_libdir}/libcie-pkcs11.so
%{_datadir}/pixmaps/cieid.png
%{_datadir}/applications/cieid.desktop

%changelog
%autochangelog
