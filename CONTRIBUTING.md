# CONTRIBUTE

## Write a scraper

The most useful thing you can do in this repository is to create a scraper that takes one of the [sources](https://github.com/gbdev/database/issues?q=is%3Aissue+is%3Aopen+label%3Asource) full of Game Boy homebrews and spits out a valid folder structure like the one we have in this repository (`entries/` folder).

Take a look to the scrapers we already made in the `scrapers` folder.

## Manually add entries

Start by forking this repository and cloning your fork locally.

### 1. Decide the game `slug` 

Decide a "slug" for the game you are adding. It's like an username: short, no spaces, special characters, or punctuation other than hyphens and underscores. It may start with a letter or digit.

> If the game is called "Super Roto Land I: Tales from the Dumper", a good slug would be `super-roto-land-1`.

### 2. Create the game folder and add the related files 

Add the decided game slug in the `gamesList.json` file and create, in the `entries` directory, a folder with the slug as name.

> E.g. `gamesList.json` will now contain `"super-roto-land-1` as element, and we created a folder named `super-roto-land-1` in `entries/`

In the created folder, put:

- The game ROM (.gb or .gbc);
- The screenshots (PNG, JPG and BMP are supported). At least 1 screenshot is required;
- Possibily, a license file (`license.txt` or `license.md`), describing the terms under which the game/assets are released, this is generally not necessary if you specify the license name.

### 3. Add the `game.json` file 

In the folder we just created, create a file called `game.json`:

```
{
    "title": "",
    "slug": "",
    "license": "",
    "developer": "",
    "repository": "",
    "platform": "",
    "typetag": "",
    "tags": [ ],
    "screenshots" : [ ],
    "rom" : ""
}
```

Fill in every property. You can take a look at existing games or the [`game.json` schema](game-schema-d3.json) to make sure everything is correct.
[The `ucity` entry](entries/ucity/game.json) is an example of a correct `game.json`.

#### Required Fields

| Property      | Description                                                          | Possible values                                         |
|---------------|----------------------------------------------------------------------|---------------------------------------------------------|
| title         | The complete name, including spacing.                                | String                                                  |
| slug          | A short identificative name that will be the in the URL              | String, Only letters, underscores, dashes and numbers   |
| developer     | Name of the developer                                                | String                                                  |
| platform      | Target console                                                       | String: `GB` or `GBC`                                   |
| typetag       | The type of the software                                             | String: `game`, `homebrew`, `demo` or `hackrom`         |
| screenshots   | A list of the filenames of the screenshots in the folder             | Array of String of the screnshots file names (no path)  |
| rom           | The name of the ROM in the folder                                    | String (no path)                                        |

The `platform` specifies the minimum requirement. For a dual-mode entry (compatible with Game Boy and including Game Boy Color or Super Game Boy enhancement), use `GB`.

#### Optional Fields

The following fields are appreciated, but not strictly required:

| Property      | Description                                                          | Possible values                                         |
|---------------|----------------------------------------------------------------------|---------------------------------------------------------|
| license       | Identifier of the license under whose terms the software is released | [Identifier](https://spdx.org/licenses/) of the license |
| assetLicense  | Identifier of the license under whose terms the assets are released  | [Identifier](https://spdx.org/licenses/) of the license |
| description   | A description of the entry                                           | String                                                  |
| video         | URL of a gameplay or trailer video on YouTube or elsewhere           | String, URI                                             |
| date          | The date the *first* version of the entry was released               | String, formatted as `YYYY-MM-DD` (ISO 8601)            |
| tags          | A list of the categories representing the entry                      | Array of String of existing categories                  |
| alias         | A list of other names with which the entry can be referred to        | Array of String                                         |
| repository    | Repository or URL where the source can be found                      | String, URI                                             |
| gameWebsite   | Game website/page                                                    | String, URI                                             |
| devWebsite    | Developer personal website/page                                      | String, URI                                             |
| onlineplay    | Allow or not the game to be played directly on the website           | Boolean                                                 |
| wip           | Flag a game as work-in-progress (not yet completely stable/bugfree)  | Boolean                                                 | 
| files         | Related files with (optional) description                            | Array of 2-d Arrays E.g. (`[["file1.zip", "description of file1.zip"],["file2.zip", "description of file2.zip"],["file3.zip"]]`)|

The `date` refers to the first public release of a project, not the release of the current version or the date it was added to the database.<!-- (A future version of the schema is expected to include the release of the current version.) -->

The possible categories for `tags` are: `RPG`, `Open Source`, `Adventure`, `Action`, `Puzzle`, `Platform`.

> E.g. If we added 2 screenshots named `screenshot1.png` and `screenshot2.png` and a ROM named `game.gbc`, the folder structure will look like this:
>
>```
>database/
>├── gamesList.json
>├── entries/
>|   └── my-new-game/
>│      ├── my-game.gb
>│      ├── screenshot1.png
>│      ├── screenshot2.png
>│      └── game.json
>```
>
> Our `game.json` will look like this:
> 
>```
>{
>    "title": "Super Roto Land 1",
>    "slug": "super-roto-land",
>    "license": "GPLv3",
>    "developer": "Emanuele Rotto",
>    "repository": "https://github.com/dubrotto/gbrottoland",
>    "platform": "gbc",
>    "typetag": "game",
>    "tags": [ "Platform", "Puzzle" ],
>    "screenshots" : [ "screenshot1.png", "screenshot2.png" ],
>    "rom" : "game.gbc"
>}
>```


### 4. Check your changes and create a PR

Check the existing folders to have examples of valid entries.

The final folder structure will look like this:

```
database/
├── gamesList.json
├── entries/
|   ├── my-new-game/
|   │   ├── my-game.gb
|   │   ├── screenshot1.png
|   │   ├── screenshot2.png
|   │   └── game.json
|   ├── another-game/
|   │   ├── my-game.gb
|   │   ├── screenshot1.png
|   │   ├── screenshot2.png
|   │   └── game.json
|   ├── another-roto-game/
|   │   ├── my-game.gb
|   │   ├── screenshot1.png
|   │   ├── screenshot2.png
|   │   └── game.json
|   |
|   ├── [...]
|   |
|
```

You're welcome to **edit**, **correct** or **improve** existing entries.
After you're finished and you're sure everything is valid (screenshot and rom names must be identical to the file names you added in the folder) you can commit your changes and propose a Pull Request.
