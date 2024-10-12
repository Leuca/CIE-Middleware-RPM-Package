FROM fedora

# Install tools
RUN dnf install -y rpm-build rpmdevtools rpmautospec curl git

# Create user
RUN useradd -m builder

# Setup the RPM build tree
USER builder
RUN rpmdev-setuptree

# Create project directory
RUN mkdir /home/builder/project

# Download sources
WORKDIR /home/builder/rpmbuild/SOURCES
RUN --mount=source=.,destination=/home/builder/project,ro,z curl -O $(spectool -S /home/builder/project/cie-middleware.spec 2>/dev/null | grep Source0 | cut -d" " -f 2)
RUN --mount=source=.,destination=/home/builder/project,ro,z curl -O $(spectool -S /home/builder/project/cie-middleware.spec 2>/dev/null | grep Source4 | cut -d" " -f 2)

# Generate specfile with correct versioning
WORKDIR /home/builder/project
RUN --mount=source=.,destination=/home/builder/project,ro,z git config --global --add safe.directory /home/builder/project
RUN --mount=source=.,destination=/home/builder/project,ro,z git status
RUN --mount=source=.,destination=/home/builder/project,ro,z rpmautospec process-distgit cie-middleware.spec /home/builder/rpmbuild/SPECS/cie-middleware.spec

# Copy sources
RUN --mount=source=.,destination=/home/builder/project,ro,z cp -rf /home/builder/project/* /home/builder/rpmbuild/SOURCES
RUN rm /home/builder/rpmbuild/SOURCES/cie-middleware.spec

WORKDIR /home/builder/rpmbuild

# Run container until stopped
CMD exec /bin/bash -c "trap : TERM INT; sleep infinity & wait"
