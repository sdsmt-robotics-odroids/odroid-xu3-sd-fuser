Name:           odroid-xu3-sd-fuser
Version:        0.2.0
Release:        1%{?dist}
Summary:        Boot media blob for ODROID-XU3

Group:          System Environment/Base
License:        BSD
URL:            http://odroid.com/dokuwiki/doku.php?id=en:odroid-xu3
Source0:        https://github.com/hardkernel/u-boot/raw/odroidxu3-v2012.07/sd_fuse/hardkernel/bl1.bin.hardkernel
Source1:        https://github.com/hardkernel/u-boot/raw/odroidxu3-v2012.07/sd_fuse/hardkernel/bl2.bin.hardkernel
Source2:        https://github.com/hardkernel/u-boot/raw/odroidxu3-v2012.07/sd_fuse/hardkernel/tzsw.bin.hardkernel
Source3:        odroid-xu3-sd-fuser
Source4:        odroid-xu3-emmc-fuser

BuildArch:      noarch

BuildRequires:  odroid-xu3-uboot

%description
Binary blob used to boot Hardkernel's ODROID-XU3. The blob contains:
- bl1
- bl2
- u-boot
- TrustZone

%prep
cp -a %{SOURCE3} odroid-xu3-sd-fuser
cp -a %{SOURCE4} odroid-xu3-emmc-fuser

%build
signed_bl1_position=0
bl2_position=30
uboot_position=62
tzsw_position=718
env_position=1230

#<BL1 fusing>
echo "BL1 fusing"
dd if=%{SOURCE0} of=bootblob.bin seek=$signed_bl1_position
#<BL2 fusing>
echo "BL2 fusing"
dd if=%{SOURCE1} of=bootblob.bin seek=$bl2_position
#<u-boot fusing>
echo "u-boot fusing"
dd if=/boot/uboot/u-boot.bin of=bootblob.bin seek=$uboot_position
#<TrustZone S/W fusing>
echo "TrustZone S/W fusing"
dd if=%{SOURCE2} of=bootblob.bin seek=$tzsw_position
#<u-boot env default>
echo "u-boot env erase"
dd if=/dev/zero of=bootblob.bin seek=$env_position count=32

chmod +x bootblob.bin

sed -i 's!@bootblobpath@!%{_datadir}/%{name}/bootblob.bin!g' odroid-xu3-sd-fuser
sed -i 's!@bootblobpath@!%{_datadir}/%{name}/bootblob.bin!g' odroid-xu3-emmc-fuser

%install
install -p -m0755 -D bootblob.bin %{buildroot}%{_datadir}/%{name}/bootblob.bin
install -p -m0755 -D odroid-xu3-sd-fuser %{buildroot}%{_bindir}/odroid-xu3-sd-fuser
install -p -m0755 -D odroid-xu3-emmc-fuser %{buildroot}%{_bindir}/odroid-xu3-emmc-fuser

%files
%{_bindir}/odroid-xu3-sd-fuser
%{_bindir}/odroid-xu3-emmc-fuser
%{_datadir}/%{name}/bootblob.bin

%changelog
* Thu Apr 09 2015 Scott K Logan <logans@cottsay.net> - 0.2.0-1
- Initial package
