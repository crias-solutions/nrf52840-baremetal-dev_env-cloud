# Base image: Ubuntu 22.04 LTS
FROM mcr.microsoft.com/devcontainers/base:ubuntu-22.04

# Prevent interactive prompts during installation
ENV DEBIAN_FRONTEND=noninteractive

# ========== SYSTEM DEPENDENCIES ==========
RUN apt-get update && apt-get install -y \
    # Build tools
    make \
    gcc \
    git \
    curl \
    wget \
    unzip \
    # USB/IP tools (CRITICAL for hardware connection)
    linux-tools-generic \
    hwdata \
    usbutils \
    kmod \
    # Python for scripting
    python3 \
    python3-pip \
    python3-venv \
    # Utilities
    nano \
    vim \
    && rm -rf /var/lib/apt/lists/*

# ========== ARM GCC TOOLCHAIN ==========
# Download ARM GCC 12.2.rel1 (recommended for nRF5 SDK)
RUN wget -q https://developer.arm.com/-/media/Files/downloads/gnu/12.2.rel1/binrel/arm-gnu-toolchain-12.2.rel1-x86_64-arm-none-eabi.tar.xz \
    && tar -xf arm-gnu-toolchain-12.2.rel1-x86_64-arm-none-eabi.tar.xz -C /opt/ \
    && rm arm-gnu-toolchain-12.2.rel1-x86_64-arm-none-eabi.tar.xz

# Add ARM GCC to PATH
ENV PATH="/opt/arm-gnu-toolchain-12.2.rel1-x86_64-arm-none-eabi/bin:${PATH}"

# ========== nRF5 SDK v17.1.0 ==========
RUN mkdir -p /opt/nrf5_sdk
WORKDIR /opt/nrf5_sdk

# Download and flatten the SDK structure
RUN wget -q https://nsscprodmedia.blob.core.windows.net/prod/software-and-other-downloads/sdks/nrf5/binaries/nrf5_sdk_17.1.0_ddde560.zip \
    && unzip -q nrf5_sdk_17.1.0_ddde560.zip \
    && mv nRF5_SDK_17.1.0_ddde560/* . \
    && rm -rf nRF5_SDK_17.1.0_ddde560 nrf5_sdk_17.1.0_ddde560.zip

# Set SDK environment variable
ENV NRF5_SDK_PATH=/opt/nrf5_sdk

# Configure SDK to use our ARM GCC toolchain (now the path exists!)
RUN echo "GNU_INSTALL_ROOT := /opt/arm-gnu-toolchain-12.2.rel1-x86_64-arm-none-eabi/bin/" > /opt/nrf5_sdk/components/toolchain/gcc/Makefile.posix \
    && echo "GNU_VERSION := 12.2.1" >> /opt/nrf5_sdk/components/toolchain/gcc/Makefile.posix \
    && echo "GNU_PREFIX := arm-none-eabi" >> /opt/nrf5_sdk/components/toolchain/gcc/Makefile.posix

# ========== nRF COMMAND LINE TOOLS ==========
# Install nrfjprog (for flashing firmware)
RUN wget -q https://nsscprodmedia.blob.core.windows.net/prod/software-and-other-downloads/desktop-software/nrf-command-line-tools/sw/versions-10-x-x/10-24-2/nrf-command-line-tools_10.24.2_amd64.deb \
    && dpkg -i nrf-command-line-tools_10.24.2_amd64.deb || apt-get install -f -y \
    && rm nrf-command-line-tools_10.24.2_amd64.deb

# ========== SEGGER J-LINK ==========
# Install J-Link software (for debugging)
RUN wget -q --post-data "accept_license_agreement=accepted" -O JLink.deb https://www.segger.com/downloads/jlink/JLink_Linux_x86_64.deb \
    && dpkg -i JLink.deb || apt-get install -f -y \
    && rm JLink.deb

# ========== PYTHON DEPENDENCIES ==========
RUN pip3 install --no-cache-dir \
    pyserial \
    click \
    colorama

# ========== WORKSPACE SETUP ==========
WORKDIR /workspaces/project

# Switch to non-root user for security
USER vscode

# Set default shell
SHELL ["/bin/bash", "-c"]
