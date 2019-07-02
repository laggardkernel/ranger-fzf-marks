# ranger-fzf-marks

[![License: MIT][license icon]][license]

A [ranger][ranger] plugin ported from [urbainvaes/fzf-marks][urbainvaes/fzf-marks].
It depends on command-line fuzzy finder [junegunn/fzf][junegunn/fzf].

## Installation
Git clone the plugins into ranger's plugins folder. (Experimental)

```bash
git clone https://github.com/laggardkernel/ranger-fzf-marks.git ~/.config/ranger/plugins/fzf-marks
```

Then add key binding for bookmark jump in `rc.conf`.

```
map <C-g> fzm
```

## Usage
Commands:
- `:fmark <markname>`, add a current dir as bookmark
- `:fzm [<optional-query-keyword>]`, jump to a bookmark
- `:dmark [<optional-query-keyword>]`, delete a bookmark

Bookmark jumping could be also be triggered with key binding like `<C-g>`.

Other features like output colorization, custom fzf command are not implemented.
This plugin only ensure basic usage of bookmark with fzf support.

## Settings
The same bookmark storage path is used from [urbainvaes/fzf-marks][urbainvaes/fzf-marks]:
`FZF_MARKS_FILE`, which defaults to `${HOME}/.fzf-marks`.

## TODO
- [x] custom storage support with `FZF_MARKS_FILE`
- [ ] delete action support in `:fzm`
- [ ] batch deletion support in `:dmark`

## License

The MIT License (MIT)

Copyright (c) 2019 laggardkernel

[license icon]: https://img.shields.io/badge/License-MIT-blue.svg
[license]: https://opensource.org/licenses/MIT
[ranger]: https://github.com/ranger/ranger
[urbainvaes/fzf-marks]: https://github.com/urbainvaes/fzf-marks
[junegunn/fzf]: https://github.com/junegunn/fzf
