cmake_minimum_required(VERSION 3.15.3)

project(cie-pkcs11)

# Look for packages
find_package(PkgConfig REQUIRED)

pkg_check_modules(CURL REQUIRED libcurl)
pkg_check_modules(BZIP2 REQUIRED bzip2)
pkg_check_modules(CRYPTOPP REQUIRED cryptopp)
pkg_check_modules(FREETYPE REQUIRED freetype2)
pkg_check_modules(PNG REQUIRED libpng)
pkg_check_modules(LIBXML2 REQUIRED libxml-2.0)
pkg_check_modules(OPENSSL REQUIRED openssl)
pkg_check_modules(PODOFO REQUIRED libpodofo)
pkg_check_modules(ZLIB REQUIRED zlib)
pkg_check_modules(FONTCONFIG REQUIRED fontconfig)
pkg_check_modules(PCSCLITE REQUIRED libpcsclite)

set(LIBCIE_DIR ${CMAKE_SOURCE_DIR}/libcie)
set(LIBCIE_SOURCE_DIR ${LIBCIE_DIR}/src)
set(LIBCIE_INCLUDE_DIR ${LIBCIE_DIR}/include)

set(CMAKE_POSITION_INDEPENDENT_CODE ON)

# Set sources
set(SDK_SRC_LIST
	${LIBCIE_SOURCE_DIR}/Base64.cpp
    ${LIBCIE_SOURCE_DIR}/BigInteger.cpp
    ${LIBCIE_SOURCE_DIR}/BigIntegerAlgorithms.cpp
    ${LIBCIE_SOURCE_DIR}/BigIntegerUtils.cpp
    ${LIBCIE_SOURCE_DIR}/BigUnsigned.cpp
    ${LIBCIE_SOURCE_DIR}/BigUnsignedInABase.cpp
    ${LIBCIE_SOURCE_DIR}/CIESigner.cpp
    ${LIBCIE_SOURCE_DIR}/CIEEngine.c
    ${LIBCIE_SOURCE_DIR}/CIEEngineHelper.c
    ${LIBCIE_SOURCE_DIR}/CertStore.cpp
    ${LIBCIE_SOURCE_DIR}/CounterSignatureGenerator.cpp
    ${LIBCIE_SOURCE_DIR}/SignatureGenerator.cpp
    ${LIBCIE_SOURCE_DIR}/LdapCrl.cpp
    ${LIBCIE_SOURCE_DIR}/M7MParser.cpp
    ${LIBCIE_SOURCE_DIR}/PdfSignatureGenerator.cpp
    ${LIBCIE_SOURCE_DIR}/PdfVerifier.cpp
    ${LIBCIE_SOURCE_DIR}/SignedDataGeneratorEx.cpp
    ${LIBCIE_SOURCE_DIR}/SignedDocument.cpp
    ${LIBCIE_SOURCE_DIR}/SignerInfoGenerator.cpp
    ${LIBCIE_SOURCE_DIR}/TSAClient.cpp
    ${LIBCIE_SOURCE_DIR}/UUCLogger.cpp
    ${LIBCIE_SOURCE_DIR}/UUCProperties.cpp
    ${LIBCIE_SOURCE_DIR}/UUCStringTable.cpp
    ${LIBCIE_SOURCE_DIR}/UUCTextFileReader.cpp
    ${LIBCIE_SOURCE_DIR}/UUCTextFileWriter.cpp
    ${LIBCIE_SOURCE_DIR}/XAdESGenerator.cpp
    ${LIBCIE_SOURCE_DIR}/XAdESVerifier.cpp
    ${LIBCIE_SOURCE_DIR}/definitions.cpp
    ${LIBCIE_SOURCE_DIR}/disigonsdk.cpp
    ${LIBCIE_SOURCE_DIR}/ASN1/ASN1BitString.cpp
    ${LIBCIE_SOURCE_DIR}/ASN1/ASN1Boolean.cpp
    ${LIBCIE_SOURCE_DIR}/ASN1/ASN1GenericSequence.cpp
    ${LIBCIE_SOURCE_DIR}/ASN1/ASN1Integer.cpp
    ${LIBCIE_SOURCE_DIR}/ASN1/ASN1Null.cpp
    ${LIBCIE_SOURCE_DIR}/ASN1/ASN1Object.cpp
    ${LIBCIE_SOURCE_DIR}/ASN1/ASN1ObjectIdentifier.cpp
    ${LIBCIE_SOURCE_DIR}/ASN1/ASN1Octetstring.cpp
    ${LIBCIE_SOURCE_DIR}/ASN1/ASN1OptionalField.cpp
    ${LIBCIE_SOURCE_DIR}/ASN1/ASN1Sequence.cpp
    ${LIBCIE_SOURCE_DIR}/ASN1/ASN1Setof.cpp
    ${LIBCIE_SOURCE_DIR}/ASN1/ASN1UTCTime.cpp
    ${LIBCIE_SOURCE_DIR}/ASN1/AlgorithmIdentifier.cpp
    ${LIBCIE_SOURCE_DIR}/ASN1/Certificate.cpp
    ${LIBCIE_SOURCE_DIR}/ASN1/CertificateInfo.cpp
    ${LIBCIE_SOURCE_DIR}/ASN1/ContentInfo.cpp
    ${LIBCIE_SOURCE_DIR}/ASN1/ContentType.cpp
    ${LIBCIE_SOURCE_DIR}/ASN1/Crl.cpp
    ${LIBCIE_SOURCE_DIR}/ASN1/DigestInfo.cpp
    ${LIBCIE_SOURCE_DIR}/ASN1/IssuerAndSerialNumber.cpp
    ${LIBCIE_SOURCE_DIR}/ASN1/Name.cpp
    ${LIBCIE_SOURCE_DIR}/ASN1/OCSPRequest.cpp
    ${LIBCIE_SOURCE_DIR}/ASN1/PKIStatusInfo.cpp
    ${LIBCIE_SOURCE_DIR}/ASN1/RSAPrivateKey.cpp
    ${LIBCIE_SOURCE_DIR}/ASN1/RSAPublicKey.cpp
    ${LIBCIE_SOURCE_DIR}/ASN1/RelativeDistinguishedName.cpp
    ${LIBCIE_SOURCE_DIR}/ASN1/SignedData.cpp
    ${LIBCIE_SOURCE_DIR}/ASN1/SignerInfo.cpp
    ${LIBCIE_SOURCE_DIR}/ASN1/SubjectPublicKeyInfo.cpp
    ${LIBCIE_SOURCE_DIR}/ASN1/TSTInfo.cpp
    ${LIBCIE_SOURCE_DIR}/ASN1/TimeStampData.cpp
    ${LIBCIE_SOURCE_DIR}/ASN1/TimeStampRequest.cpp
    ${LIBCIE_SOURCE_DIR}/ASN1/TimeStampResponse.cpp
    ${LIBCIE_SOURCE_DIR}/ASN1/TimeStampToken.cpp
    ${LIBCIE_SOURCE_DIR}/ASN1/UUCBufferedReader.cpp
    ${LIBCIE_SOURCE_DIR}/ASN1/UUCByteArray.cpp
    ${LIBCIE_SOURCE_DIR}/RSA/desc.c
    ${LIBCIE_SOURCE_DIR}/RSA/nn.c
    ${LIBCIE_SOURCE_DIR}/RSA/r_encode.c
    ${LIBCIE_SOURCE_DIR}/RSA/r_stdlib.c
    ${LIBCIE_SOURCE_DIR}/RSA/rc2.c
    ${LIBCIE_SOURCE_DIR}/RSA/rc2.h
    ${LIBCIE_SOURCE_DIR}/RSA/rsa.c
    ${LIBCIE_SOURCE_DIR}/RSA/sha1.c
    ${LIBCIE_SOURCE_DIR}/RSA/sha2.c
    ${LIBCIE_SOURCE_DIR}/CSP/IAS.cpp
    ${LIBCIE_SOURCE_DIR}/CSP/ATR.cpp
    ${LIBCIE_SOURCE_DIR}/CSP/ExtAuthKey.cpp
    ${LIBCIE_SOURCE_DIR}/PCSC/APDU.cpp
    ${LIBCIE_SOURCE_DIR}/PCSC/CardLocker.cpp
    ${LIBCIE_SOURCE_DIR}/PCSC/PCSC.cpp
    ${LIBCIE_SOURCE_DIR}/PCSC/Token.cpp
    ${LIBCIE_SOURCE_DIR}/Util/Array.cpp
    ${LIBCIE_SOURCE_DIR}/Util/CacheLib.cpp
    ${LIBCIE_SOURCE_DIR}/Util/CryptoppUtils.cpp
    ${LIBCIE_SOURCE_DIR}/Util/funccallinfo.cpp
    ${LIBCIE_SOURCE_DIR}/Util/IniSettings.cpp
    ${LIBCIE_SOURCE_DIR}/Util/log.cpp
    ${LIBCIE_SOURCE_DIR}/Util/ModuleInfo.cpp
    ${LIBCIE_SOURCE_DIR}/Util/TLV.cpp
    ${LIBCIE_SOURCE_DIR}/Util/util.cpp
    ${LIBCIE_SOURCE_DIR}/Util/UtilException.cpp
	${LIBCIE_SOURCE_DIR}/Util/SyncroEvent.cpp
    ${LIBCIE_SOURCE_DIR}/Util/SyncroMutex.cpp
    ${LIBCIE_SOURCE_DIR}/Crypto/AES.cpp
    ${LIBCIE_SOURCE_DIR}/Crypto/ASNParser.cpp
    ${LIBCIE_SOURCE_DIR}/Crypto/Base64.cpp
    ${LIBCIE_SOURCE_DIR}/Crypto/DES3.cpp
    ${LIBCIE_SOURCE_DIR}/Crypto/MAC.cpp
    ${LIBCIE_SOURCE_DIR}/Crypto/MD5.cpp
    ${LIBCIE_SOURCE_DIR}/Crypto/RSA.cpp
    ${LIBCIE_SOURCE_DIR}/Crypto/SHA1.cpp
    ${LIBCIE_SOURCE_DIR}/Crypto/SHA256.cpp
    ${LIBCIE_SOURCE_DIR}/Crypto/SHA512.cpp
    )

set(LIBCIE_SRC_LIST
    ${LIBCIE_SOURCE_DIR}/CSP/AbilitaCIE.cpp
    ${LIBCIE_SOURCE_DIR}/CSP/FirmaConCIE.cpp
    ${LIBCIE_SOURCE_DIR}/CSP/PINManager.cpp
    ${LIBCIE_SOURCE_DIR}/CSP/VerificaConCIE.cpp
    ${LIBCIE_SOURCE_DIR}/Sign/CIESign.cpp
    ${LIBCIE_SOURCE_DIR}/Sign/CIEVerify.cpp
    ${LIBCIE_SOURCE_DIR}/PKCS11/CardContext.cpp
    ${LIBCIE_SOURCE_DIR}/PKCS11/CardTemplate.cpp
    ${LIBCIE_SOURCE_DIR}/PKCS11/CIEP11Template.cpp
    ${LIBCIE_SOURCE_DIR}/PKCS11/initP11.cpp
    ${LIBCIE_SOURCE_DIR}/PKCS11/Mechanism.cpp
    ${LIBCIE_SOURCE_DIR}/PKCS11/P11Object.cpp
    ${LIBCIE_SOURCE_DIR}/PKCS11/PKCS11Functions.cpp
    ${LIBCIE_SOURCE_DIR}/PKCS11/session.cpp
    ${LIBCIE_SOURCE_DIR}/PKCS11/Slot.cpp
    ${LIBCIE_SOURCE_DIR}/LOGGER/Logger.cpp
    )


# Set include dirs
set(LIBCIE_INCLUDE_LIST
	${LIBCIE_INCLUDE_DIR}
	${LIBCIE_SOURCE_DIR}/ASN1
    ${LIBCIE_SOURCE_DIR}
    ${LIBCIE_SOURCE_DIR}/RSA
    ${LIBCIE_SOURCE_DIR}/CSP
    ${LIBCIE_SOURCE_DIR}/Sign
    ${LIBCIE_SOURCE_DIR}/PKCS11
    ${LIBCIE_SOURCE_DIR}/LOGGER
	${LIBCIE_SOURCE_DIR}/Util
    ${LIBCIE_SOURCE_DIR}/PCSC
    ${LIBCIE_SOURCE_DIR}/Crypto
    )

set(INCLUDE_LIST_SHARED
    /usr/include/
    ${PODOFO_INCLUDE_DIRS}
    ${CRYPTOPP_INCLUDE_DIRS}
    ${FREETYPE_INCLUDE_DIRS}
    ${CURL_INCLUDE_DIRS}
    ${PNG_INCLUDE_DIRS}
    ${OPENSSL_INCLUDE_DIRS}
    ${PCSCLITE_INCLUDE_DIRS}
    ${ZLIB_INCLUDE_DIRS}
    ${LIBXML2_INCLUDE_DIRS}
    )

# Set libraries list
set(LIBRARIES_LIST
    curl
    bz2
    cryptopp
    freetype
    png16
    xml2
    crypto
    z
    fontconfig
    pcsclite
    podofo
    )

add_library(${PROJECT_NAME} SHARED ${SDK_SRC_LIST} ${LIBCIE_SRC_LIST})
target_link_libraries(${PROJECT_NAME} PRIVATE ${LIBRARIES_LIST})
target_include_directories(${PROJECT_NAME} PRIVATE ${INCLUDE_LIST_SHARED} ${LIBCIE_INCLUDE_LIST})

include(GNUInstallDirs)
install(TARGETS ${PROJECT_NAME} DESTINATION "${CMAKE_INSTALL_LIBDIR}")
