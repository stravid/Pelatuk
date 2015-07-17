**This is a work in progress.**

### Install
1. `cd ~/Library/Application Support/Sublime Text 3/Packages/`
2. `git clone https://github.com/stravid/Pelatuk.git`

### Use
`ctrl + alt + l` -> Run all tests
`ctrl + alt + k` -> Run current test file
`ctrl + alt + j` -> Run test of cursor position
`ctrl + alt + h` -> Run last test

### Known Issues
If Pelatuk keeps opening new terminal windows when a test run is triggered it
can be that ZSH or something similar overwrites the terminal windows title.
In such a case Pelatuk can not find the previously opened window an opens a new
one.
