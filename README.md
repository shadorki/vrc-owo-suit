# vrc-owo-suit

A python application for VRChat players to use OWO Suits in game

## Table of Contents

- [Installation](#installation)
- [Contributing](#contributing)

## Installation

---

Head over to the [Releases](https://github.com/uzair-ashraf/vrc-owo-suit/releases) page to get the latest release.

- Download the executable and run it after you start VRChat.
- Download the Unity Package and add the Prefab to your avatar. ([More Instructions](#setting-up-your-avatar) on this below)

## Contributing

---

### Requirements

- Python 3.10.9
- Windows 10
- OWO Suit

1. Clone the repository

   ```shell
   git clone git@github.com:uzair-ashraf/vrc-owo-suit.git
   cd vrc-owo-suit
   ```

1. Install Dependencies

   ```shell
   pip install -r requirements.txt
   ```

1. Run

   ```shell
   python main.py
   ```

1. Build a standalone executable

   This repository is setup with a Github action to compile the standalone executable. If you would like to compile it on your local machine you can read the action for the command via `pyinstaller` [here](./.github/workflows/release.yml).

## Setting up your avatar



## Notes

So it looks like when I send a sensation it cancels out the previous one

Looks Like what I'll have to do is keep track of what sensations are in contact, and if they end up being triggered then I can chain them directly