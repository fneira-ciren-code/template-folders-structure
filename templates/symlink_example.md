# Symbolic links for external data

Keep large or shared datasets outside the project and link them into the data folders.

**Rule: link inside the folder, do not replace the folder.** Replacing `data/raw` removes
the tracked `data/raw/.gitkeep` from git. Create the link as a child of the folder instead:

- Good: `data/raw/dataset` -> `/external/drive/dataset`
- Bad: `data/raw` -> `/external/drive/`

Links under `data/` are ignored by git (`data/**` in `.gitignore`).
Check with `git check-ignore -v data/raw/dataset`.

## Linux and macOS (no administrator rights needed)

Create a link:

```sh
ln -s /absolute/path/to/dataset data/raw/dataset
```

Replace an existing link (`-n` treats a link to a directory as a file):

```sh
ln -sfn /absolute/path/to/other data/raw/dataset
```

Inspect:

```sh
ls -l data/raw
readlink data/raw/dataset
```

Remove the link (no trailing slash; this removes only the link, not the target):

```sh
rm data/raw/dataset
```

Use `sudo` only to write to protected locations. Links inside the project never need it.

## Windows

Windows has four link types with different requirements:

| Type | Needs admin or Developer Mode | Works across drives | Command (cmd) | Command (PowerShell) |
|---|---|---|---|---|
| Directory junction | No | No (local drives, absolute path) | `mklink /J` | `New-Item -ItemType Junction` |
| Directory symlink | Yes | Yes | `mklink /D` | `New-Item -ItemType SymbolicLink` |
| File symlink | Yes | Yes | `mklink` | `New-Item -ItemType SymbolicLink` |
| File hard link | No | No (same volume) | `mklink /H` | `New-Item -ItemType HardLink` |

Without administrator rights, symlinks need **Developer Mode**: Settings > For developers
(Windows 11: System > For developers). Junctions do not need it.

Junction, no administrator rights (cmd):

```bat
mklink /J data\raw\dataset C:\external\dataset
```

Junction (PowerShell):

```powershell
New-Item -ItemType Junction -Path data\raw\dataset -Target C:\external\dataset
```

Directory symlink, with administrator rights or Developer Mode (cmd):

```bat
mklink /D data\raw\dataset C:\external\dataset
```

Directory symlink (PowerShell):

```powershell
New-Item -ItemType SymbolicLink -Path data\raw\dataset -Target C:\external\dataset
```

Inspect and remove:

```bat
dir /AL data\raw
rmdir data\raw\dataset
```

`rmdir` removes the link, not the target directory.

> The Windows commands above are documented behavior. They were **not run** on the machine
> where this template was built.

## Python and R (portable)

Python (raises `OSError` on Windows without the privilege):

```python
from pathlib import Path

Path("data/raw/dataset").symlink_to(
    "/absolute/path/to/dataset", target_is_directory=True
)
```

R (returns `FALSE` instead of stopping when the link cannot be created):

```r
file.symlink("/absolute/path/to/dataset", "data/raw/dataset")
```
