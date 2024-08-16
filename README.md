👋 Hi, I’m Jeroen Taverne

I have created a multi purpose cartridge for MSX computers. It's based on a Raspberry Pi Pico clone with 16MB of FLASH memory and 256 kBytes of RAM.

**Firmware releases: https://github.com/jeroentaverne/msxpico/releases**

**For demos running on real hardware check: https://www.youtube.com/@MSXPico**

**Discord server: https://discord.com/invite/Dn6g9Ek5tK**

# MSX Pico cartridge features

- 3D printed cartridge case in available colors
- PCB with gold plated contacts.
- Built in menu
- Stereo 3.5mm audio output
- FM-PAC sound en SRAM emulation
- Konami SCC+ sound emulation
- Dual PSG sound emulation
- MP3 player
- Volume en mono/stereo setting
- Micro SD card slot
- USB-C connector for software update
- RGB status LED
- Optional MIDI output
- Nextor built in with at most 224kB extra RAM
- ROM files till 15MB supported
- DSK files till 720kB supported (multi disk support is in development)
- ASCII, Konami, NEO mapper support
- For MSX2, MSX2+, Turbo-R computers
- Works on most MSX1 computers (VG8020/00 has an issue)
- Sony XV-T550 support

**Features can be enabled/disabled in the configuration screen**

**For a questions, ideas and orders please contact: msxpico@gmail.com**

# Operation

Never insert or remove the cartridge when the MSX is powered on!
 
## Built in menu
After inserting the cartridge and power up a selection menu is shown on screen. All these items can be started without a SD card inserted. For help with Nextor please check the Nextor website.

By pressing the right cursor key the SD card contents is shown. In this screen the following files can be started:

-	.ROM files (support for standard ROMs, ASCII 8, ASCII 16, Konami without SCC and Konami with SCC sound)
-	.DSK single disk files up to 720kB (for multi disk support please use Nextor together with Sofarun)
-	.MP3 and .WAV files (48 kHz max)

## Help screen
Help page is shown by pressing the H key

## Configuration screen
Configuration screen is shown with SHIFT+H key.

## Sorting
Sorting switch between alphabetic and size with SELECT key.

## Extra RAM
With some options like Nextor extra RAM memory mapper is available. The size depends if SCC+ and/or FM-PAC are enabled in the configuration screen.

## RGB LED
The RGB LED can be enabled or disabled in the configuration screen.

-	Purple when connected to PC by USB-C for software update
-	Green steady when software update is finished
-	Green blink when SD card is accessed when Nextor is used
-	Red blink when MSX is reset
-	Blue blink when MIDI data is sent
-	White fading when audio is played

## MIDI output
The MIDI output is optional. When the MSX Pico supports MIDI out, it needs to be enabled in the configuration screen. Midry v1.06 running on Nextor can be used to play MIDI files.

## Dual PSG emulation
Dual PSG is supported in some games and in vgmplay.

## FM-PAC emulation
The FM-PAC emulation needs to be enabled in the configuration screen. When the FM-PAC is enabled, it's also possible to use the load/save feature of the FM-PAC in games started from SD card.

## SCC+ emulation
The SCC+ emulation currently involves the sound chip only. Konami ROMs will work without any modifications. VGMPLAY and SOFARUN can detect the SCC+ without any issues. To be able to detect the SCC+ properly by for instance SD Snatcher, the modified version of game need to be used. This might also apply to other games or demos.

## MP3 playback
MP3 files in mono or stereo with a maximum of 48kHz can be played back.

## Software update
- Download latest .uf2 update file from github.com/jeroentaverne/msxpico
- Turn off MSX
- Remove MSX Pico from MSX, or keep it inserted
- Connect MSX Pico to a PC/Apple/Linux computer using a USB-C cable
- RGB LED should turn PURPLE
- An extra USB drive should show up in explorer/finder
- Copy the .uf2 update file to the USB drive
- Updating will start
- After updating the RGB LED will turn GREEN

## Create bootable SD card
- Insert MSX Pico
- Power on the MSX
- Select Nextor
- Insert new SD card
- In BASIC type: call fdisk
- Select the SD card
- Delete all partitions by pressing D key
- Create at least one new partition by pressing A key
- Write the parititions by pressing W key
- Power off the MSX
- Copy the contents of msxpico_sd.zip to the first partition using a PC or MAC
