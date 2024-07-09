## Flask endpoints

### Valorant:
#### Ranked Leaderboard: `/valorant/leaderboard/<region>/<toUpdate>`
Parameter Options:

| Parameter | Type   | Required | Description                      | Options                         |
| --------- | ------ | -------- | -------------------------------- | ------------------------------- |
| region    | String | Yes      | Region to fetch leaderboard for  | [ap, eu, kr, na, local]         |
| toUpdate  | String | No       | Whether to update local database | [true, false] \| Default: false |

Response:

| Name        | Type   | Description                           |
| ----------- | ------ | ------------------------------------- |
| title       | String | Title of leaderboard                  |
| leaderboard | String | Leaderboard entries separated by `\n` |

#### Account Statistics: `/valorant/stats/<ign>/<tag>`
Parameter Options:

| Parameter | Type   | Required | Description                                                                                                       |
| --------- | ------ | -------- | ----------------------------------------------------------------------------------------------------------------- |
| ign       | String | Yes      | Riot in-game name (first section of username in `ign#tag` format)                                                 |
| tag       | String | No       | Riot tag, (second section of username in `ign#tag` format). Not required if account in database \| Default: false |

Response:

| Name      | Type      | Description                                             |
| --------- | --------- | ------------------------------------------------------- |
| author    | String    | Username of player in `ign#tag` format                  |
| thumbnail | String    | URL to in-game banner (small format)                    |
| acts      | [Dict]    | Act-rank for each act. Keys of each item: [name, value] |
#### Account Banner: `/valorant/banner/<ign>/<tag>`
Parameter Options:

| Parameter | Type   | Required | Description                                                                                                       |
| --------- | ------ | -------- | ----------------------------------------------------------------------------------------------------------------- |
| ign       | String | Yes      | Riot in-game name (first section of username in `ign#tag` format)                                                 |
| tag       | String | No       | Riot tag, (second section of username in `ign#tag` format). Not required if account in database \| Default: false |

Response:

| Name      | Type      | Description                                             |
| --------- | --------- | ------------------------------------------------------- |
| author    | String    | Username of player in `ign#tag` format                  |
| thumbnail | String    | URL to in-game banner (small format)                    |
| acts      | Dict List | Act-rank for each act. Keys of each item: [name, value] |
#### MMR Graph: `/valorant/graph/<ign_list>/<acts>`
Parameter Options:

| Parameter | Type   | Required | Description                                                                        | Options                         |
| --------- | ------ | -------- | ---------------------------------------------------------------------------------- | ------------------------------- |
| ign_list  | String | Yes      | Comma separated Riot in-game names (first section of username in `ign#tag` format) |                                 |
| acts      | String | No       | Whether to mark acts on graph                                                      | [true, false] \| Default: false |

Response:

| Name     | Type   | Description                    |
| -------- | ------ | ------------------------------ |
| content  | String | Last update date/error message |
| filepath | String | File path to image of graph    |
### MyAnimeList:

#### Anime information: `/mal/info/anime/<type>/<title>`
Parameter Options:

| Parameter | Type   | Required | Description           | Options                                                                  |
| --------- | ------ | -------- | --------------------- | ------------------------------------------------------------------------ |
| type      | String | No       | Category to search in | [tv, movie, ova, special, ona, music, cm, pv, tv_special] \| Default: tv |
| title     | String | Yes      | Title of anime        |                                                                          |

Response:

| Name           | Type     | Description                                      |
| -------------- | -------- | ------------------------------------------------ |
| url            | String   | Link to entry on MyAnimeList                     |
| eng_title      | String   | Title in English                                 |
| jap_title      | String   | Title in Japanese                                |
| score          | Int      | Average MyAnimeList score                        |
| synopsis       | String   | Synopsis from MyAnimeList                        |
| ep_count       | String   | Number of episodes (`?` if show is still airing) |
| Airing_Dates   | String   | Dates the show aired                             |
| type           | String   | Anime type (same options as `type` parameter)    |
| source         | String   | Type of source material                          |
| sequel         | [String] | List of sequels                                  |
| opening_themes | [String] | List of opening themes                           |
| ending_themes  | [String] | List of ending themes                            |
| genres         | String   | Anime's genres (comma separated)                 |
| studios        | String   | Anime's studios (comma separated)                |
| licensors      | String   | Anime's licensors (comma separated)              |
| image_url      | String   | URL to poster artwork                            |
#### Manga information: `/mal/info/manga/<title>`
Parameter Options:

| Parameter | Type   | Required | Description    |
| --------- | ------ | -------- | -------------- |
| title     | String | Yes      | Title of manga |

Response:

| Name           | Type   | Description                                                |
| -------------- | ------ | ---------------------------------------------------------- |
| url            | String | Link to entry on MyAnimeList                               |
| eng_title      | String | Title in English                                           |
| jap_title      | String | Title in Japanese                                          |
| score          | String | Average MyAnimeList score                                  |
| rank           | Int    | Ranking of manga on MyAnimeList                            |
| synopsis       | String | Synopsis from MyAnimeList                                  |
| chap_count     | String | Number of chapters (`?` if manga is still being published) |
| vol_count      | String | Number of volumes (`?` if manga is still being published)  |
| publishing     | String | Dates the manga was published                              |
| type           | String | Type of manga                                              |
| genres         | String | Manga's genres (comma separated)                           |
| authors        | String | Authors of the manga                                       |
| serializations | String | Serializations of the manga                                |
| image_url      | String | URL to poster artwork                                      |
#### Character information: `/mal/info/character/<name>`
Parameter Options:

| Parameter | Type   | Required | Description       |
| --------- | ------ | -------- | ----------------- |
| name      | String | Yes      | name of character |

Response:

| Name         | Type     | Description                                         |
| ------------ | -------- | --------------------------------------------------- |
| url          | String   | Link to entry on MyAnimeList                        |
| name         | String   | Name of character                                   |
| favorites    | Int      | Number of people who have favourited on MyAnimeList |
| description  | String   | Character description                               |
| anime        | [String] | List of anime appearances                           |
| manga        | [String] | List of manga appearances                           |
| voice_actors | [tuple]  | List of voice actors in format: (name, language)    |
| image_url    | String   | URL to image of character from MyAnimeList          |
#### Vote Distribution Graph: `/mal/graph/<category>/<type>/<title>`
Parameter Options:

| Parameter | Type   | Required | Description                 | Options                                                                  |
| --------- | ------ | -------- | --------------------------- | ------------------------------------------------------------------------ |
| category  | String | Yes      | anime or manga              | [anime, manga]                                                           |
| type      | String | No       | Type of anime to search for | [tv, movie, ova, special, ona, music, cm, pv, tv_special] \| Default: tv |
| title     | String | Yes      | Title of anime/manga        |                                                                          |

Response:

| Name          | Type   | Description                                                                |
| ------------- | ------ | -------------------------------------------------------------------------- |
| url           | String | Link to entry on MyAnimeList                                               |
| filepath      | String | File path to image of graph                                                |
| title         | String | Title of anime/manga                                                       |
| completed     | String | Number of people who have completed it                                     |
| on_hold       | String | Number of people who have put it on hold                                   |
| dropped       | String | Number of people who have dropped it                                       |
| total         | String | Total number of members                                                    |
| watching      | String | Number of people who are watching it (returned only if `category=anime` )  |
| plan_to_watch | String | Number of people who plan to watch it (returned only if `category=anime` ) |
| reading       | String | Number of people who are reading it (returned only if `category=manga` )   |
| plan_to_read  | String | Number of people who plan to read it (returned only if `category=manga` )  |
### Other:

#### Rickies Chairmen: `/other/connected`
Response:

| Name        | Type   | Description                                                                                            |
| ----------- | ------ | ------------------------------------------------------------------------------------------------------ |
| title       | String | A title                                                                                                |
| url         | String | Link to show                                                                                           |
| chairmen    | [Dict] | List of current chairmen. Keys for each item: [name (position title), value (name of position holder)] |
| image_url   | String | URL to artwork                                                                                         |