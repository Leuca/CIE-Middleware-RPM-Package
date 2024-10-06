#!/usr/bin/env bash

java -Xms1G -Xmx1G -Dawt.useSystemAAFontSettings=on -cp /usr/lib64:/usr/share/java/CIEID/CIEID.jarPATH it.ipzs.cieid.MainApplication "${@}"
