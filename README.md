Books Concierge (2017 version)
==============================

* [What is this?](#what-is-this)
* [Assumptions](#assumptions)
* [What's in here?](#whats-in-here)
* [Project Lifcycle](#project-lifecycle)
* [Data Flow](#data-flow)
* [Books Spreadsheet Fields](#books-spreadsheet-fields)
* [Bootstrap the project](#bootstrap-the-project)
* [Hide project secrets](#hide-project-secrets)
* [Save media assets](#save-media-assets)
* [Add a page to the site](#add-a-page-to-the-site)
* [Run the project](#run-the-project)
* [COPY configuration](#copy-configuration)
* [COPY editing](#copy-editing)
* [Load books and covers](#load-books-and-covers)
* [Get iTunes IDs](#get-itunes-ids)
* [Get Goodreads IDs](#get-goodreads-ids)
* [Get Links to Member Station Coverage](#get-links-to-member-station-coverage)
* [Arbitrary Google Docs](#arbitrary-google-docs)
* [Run Python tests](#run-python-tests)
* [Run Javascript tests](#run-javascript-tests)
* [Compile static assets](#compile-static-assets)
* [Test the rendered app](#test-the-rendered-app)
* [Deploy to S3](#deploy-to-s3)
* [Report analytics](#report-analytics)

What is this?
-------------

[A snappy looking presentation of NPR contributors' favorite books of the year.](http://apps.npr.org/best-books-2017/)

This code is open source under the MIT license. See LICENSE for complete details.

Assumptions
-----------

The following things are assumed to be true in this documentation.

* You are running OSX.
* You are using Python 2.7. (Probably the version that came OSX.)
* You have [virtualenv](https://pypi.python.org/pypi/virtualenv) and [virtualenvwrapper](https://pypi.python.org/pypi/virtualenvwrapper) installed and working.
* You have NPR's AWS and other credentials stored as environment variables locally.

For more details on the technology stack used with the app-template, see our [development environment blog post](http://blog.apps.npr.org/2013/06/06/how-to-setup-a-developers-environment.html).

What's in here?
---------------

The project contains the following folders and important files:

* ``confs`` -- Server configuration files for nginx and uwsgi. Edit the templates then ``fab <ENV> servers.render_confs``, don't edit anything in ``confs/rendered`` directly.
* ``data`` -- Data files, such as those used to generate HTML.
* ``fabfile`` -- [Fabric](http://docs.fabfile.org/en/latest/) commands for automating setup, deployment, data processing, etc.
* ``etc`` -- Miscellaneous scripts and metadata for project bootstrapping.
* ``jst`` -- Javascript ([Underscore.js](http://documentcloud.github.com/underscore/#template)) templates.
* ``less`` -- [LESS](http://lesscss.org/) files, will be compiled to CSS and concatenated for deployment.
* ``templates`` -- HTML ([Jinja2](http://jinja.pocoo.org/docs/)) templates, to be compiled locally.
* ``tests`` -- Python unit tests.
* ``www`` -- Static and compiled assets to be deployed. (a.k.a. "the output")
* ``www/assets`` -- A symlink to an S3 bucket containing binary assets (images, audio).
* ``www/live-data`` -- "Live" data deployed to S3 via cron jobs or other mechanisms. (Not deployed with the rest of the project.)
* ``www/test`` -- Javascript tests and supporting files.
* ``app.py`` -- A [Flask](http://flask.pocoo.org/) app for rendering the project locally.
* ``app_config.py`` -- Global project configuration for scripts, deployment, etc.
* ``copytext.py`` -- Code supporting the [Editing workflow](#editing-workflow)
* ``crontab`` -- Cron jobs to be installed as part of the project.
* ``public_app.py`` -- A [Flask](http://flask.pocoo.org/) app for running server-side code.
* ``render_utils.py`` -- Code supporting template rendering.
* ``requirements.txt`` -- Python requirements.
* ``static.py`` -- Static Flask views used in both ``app.py`` and ``public_app.py``.

Project lifecycle
-----------------

Since this is an annual project and a collaboration between multiple teams, it's useful to know the start-to-finish process so everyone's aware of the dependencies between teams.

This is based on the timeline laid out in a conversation between Nicole Cohen and Geoff Hing in September 2017.

### Copy project code

TODO: Define when this happens.

The Visuals Team makes a copy of the project code and pushes it to a new repostory on GitHub.

* Copy project code?  TODO: Define whether this means copying files or forking the repo or something else.
* Push copy to a new GitHub repository.
* Create a new version of the copy spreadsheet.
* Create a testing version of the books spreadsheet that includes ISBN values for book records.

### January - Create a new version of the books spreadsheet

The Arts Desk creates a new version of the books spreadsheet by copying the previous years.  This happens early on in the project because staff wants to add books right away.

### Late September - Share books spreadsheet with visuals team

The arts desk shares the books spreadsheet with the visuals team.  They update the `app_config` module to reflect that sheet's document ID.

### Early October - Reach out to staff and critics

By early October, the Arts Desk will have reached out to staff and critics to write reviews. Staff is contacted first.  Staff and reviewers will call dibs on the books they want to review a few weeks after the initial call-out.

### Mid October - Send assignments

The Arts Desk sends assignments for reviews.

### Late October - Add additional book data fields

The Arts Desk will add in additional fields for book records, such as ISBNs.  They usually do this in one fell swoop and often use an intern to do the work.  Because ISBNs are required to pull cover images, the Visuals team uses a test version of the spreadsheet, usually with previous year's data to test the rig.

### End of October - All write-ups due

The Visuals Team publishes the site to staging with the most recent book list and a first pass at colors.

### Mid November - Copy editing

The Visuals Team publishes the site to staging with the most recent book list and finalized colors.

This facilitates copy editing, which is a drawn out process that goes all the way until launch.

### Late November - Generate promo image

The Visuals Team runs a script to generate the promo image, a composite of book cover images.  This happens later than sharing the staging site because the book list can change.

### Late November - Set up stub page in Seamus

The Arts Desk sets up a stub page in Seamus.  Either the Arts Desk or Visuals emails Online Tech. to tell them to redirect the stub page to the app URL.

### Late November - Tag meeting

The Arts Desk meets to determine if the tags they have selected for the books make books easy for users to discover.

Prior to this meeting, the Visuals team generates a tag audit report and republishes the site to staging.

### Late November - Get edits back from copy editors

### Before launch - Make a launch plan

Before launch, the Arts Desk coordinates with the people who produce the home page and social media teams ot make a plan for launching the site.

### Early December - Launch!

On launch day the Arts Desk pays close attention to Chartbeat and other analytics.

### Shortly after launch - Generate analytics report

The Visuals Team generates a [report](https://docs.google.com/document/d/1fLbphzWXt_I8LSf6iW7urJCBeo1B-MX5iyWIfCOH-xA/edit#) of how the app did in it's first few days that includes total traffic, unique views, info about individual tag traffic.

Data Flow
---------

TODO: Better summarize the data flow.

The books, their reviews and other metadata originate in a Google Spreadsheet, this is serialized as ? and passed to Underscore templates to render the user-facing HTML.

The book reviews start in a Google Spreadsheet.

The [Load books and covers](#load-books-and-covers) section describes the configuration needed to tell this project's code how to access the book list spreasdsheet.

The `data.load_books` Fabric task downloads the books spreadsheet as CSV and saves it as `data/books.csv`.  It then takes the downloaded CSV file, does some validation and normalization of the data (which is mostly handled inside the `Book` class) and stores the output as JSON in `www/static-data/books.json`.  The task also writes some other CSV files, but I'm not sure what they do.

A sample book entry in `www/static-data/books.json` looks like this:

```
{
  "author": "Mona Awad",
  "book_seamus_id": "472159879",
  "external_links": [],
  "hide_ibooks": "",
  "html_text": false,
  "isbn": "0143128485",
  "isbn13": "9780143128489",
  "itunes_id": "998405272",
  "links": [
    {
      "category": "Feature",
      "title": "NPR's Book Concierge: Our Guide To 2016's Great Reads",
      "url": "http://www.npr.org/2016/12/06/503179028/nprs-book-concierge-our-guide-to-2016s-great-reads"
    },
    {
      "category": "Interview",
      "title": "'You Cannot Shame Me': 2 New Books Tear Down 'Fat Girl' Stereotypes",
      "url": "http://www.npr.org/2016/03/31/472132175/you-cannot-shame-me-two-new-books-tear-down-fat-girl-stereotypes"
    },
    {
      "category": "Read an excerpt",
      "title": "",
      "url": "http://www.npr.org/472159879#excerpt"
    }
  ],
  "reviewer": "Lynn Neary",
  "reviewer_id": "correspondent, Arts Desk",
  "reviewer_link": "http://www.npr.org/people/2100948/lynn-neary",
  "slug": "13-ways-of-looking-at-a-fat-girl-fiction",
  "tags": [
    "staff-picks",
    "book-club-ideas",
    "identity-and-culture",
    "realistic-fiction"
  ],
  "teaser": "The title of this book might be off-putting \u2014 after all, the word \"fat\" makes people uncomfortable. We prefer euphemisms like \"chubby\" or \"big.\" But novelist Mona Awad ...",
  "text": "The title of this book might be off-putting \u2014 after all, the word \"fat\" makes people uncomfortable. We prefer euphemisms like \"chubby\" or \"big.\" But novelist Mona Awad uses the word deliberately. She wants her readers to understand how a struggle with body image can take over a life. Lizzie, the fat girl of the title, is an insecure, overweight young woman who lets men take advantage of her in humiliating ways. Later we meet her as an older, thin woman, obsessed with staying fit, but big or small, happiness eludes her. Awad is a fine writer with a keen sense of black humor, which makes this often sad story more entertaining than you might expect.",
  "title": "13 Ways Of Looking At A Fat Girl: Fiction"
}
```

The `render.render_all` Fabric task iterates through all the Flask views and renders them to static files.  This includes the `index` view in `app.py` which loads `www/static-data/books.json` and renders the JSON as the `window.BOOKS` JavaScript variable in a `<script>` tag near the bottom of the page.  The template rendered by this view is `templates/index.html`.

The `on_book_hash()` function in `www/js/app.js` selects a book object from the `BOOKS` array and passes it to the `JST.book_modal` template function as the `book` context variable.  That template is defined in `jst/book_modal.html`.

Books Spreadsheet Fields
------------------------

### User-facing fields

These fields are listed in the order in which they're rendered in the `jst/book_modal.html` template.

#### TITLE

Example values: `13 Ways Of Looking At A Fat Girl: Fiction`

JSON/template property: title

#### AUTHOR

JSON/template property: author

Example values: `Mona Awad`

This property is optional.


#### TAGS

JSON/template property: tags

Example values: `Mysteries & Thrillers, Staff Picks`

This property is optional.

#### text

The book desription/review.

JSON/template property: text

Example values: `Count Alexander Rostov is a resourceful man who loves the finer things in life. When he is sentenced by the Bolsheviks to a lifetime of house arrest in a tiny room in the attic of Moscow's best hotel, he uses his charm and wit to build a new life that is in some ways richer than his old one. While wars both hot and cold rage in the outside world, Count Rostov finds purpose and people to love within the confines of the Metropol. The count, says author Amor Towles, has a <a href="http:// http://www.npr.org/2016/09/06/492434255/idea-for-gentleman-in-moscow-came-from-many-nights-in-luxury-hotels" target="_blank" >will to joy.</a> No wonder, then, that <em>A Gentleman in Moscow</em> is a joyful read.`

#### html text

JSON/template property: html\_text

While referenced in the template, it doesn't appear that this value will ever be rendered by the template logic.

#### REVIEWER

JSON/template property: reviewer

Example values: `Lynn Neary`

This property is optional.

#### REVIEWER LINK

JSON/Template property: reviewer\_link

Example values: `http://www.npr.org/people/497524072/natalie-winston`

This property is optional.

#### REVIEWER ID

JSON/template property: reviewer\_id

Example values: `correspondent, Arts Desk`, `<em>Weekend Edition</em> staff`

This property is optional.

#### isbn

JSON/template property: isbn

Example values: `0812992989`

#### hide\_ibooks

JSON/template property: hide\_ibooks

Example values: ``, `TRUE`

This property is optional.

This value is populated by the visuals team.

TODO: Explain how it is populated.

#### itunes\_id

JSON/template property: itunes\_id

Example values: `998405272`

This field will not be rendered if `hide_ibooks` is `TRUE`.

It will only be used to generate the iTunes URL if the `USE_ITUNES_ID` is set to `True`.

This value is populated by the visuals team.

TODO: Explain how it is populated.

#### goodreads\_id

JSON/template property: goodreads\_id

Example values: `31915219`

This value is populated by the visuals team.

TODO: Explain how it is populated.

#### book\_seamus\_id

JSON/template property: links

Example values: `498577009`

This property is optional.

#### EXTERNAL LINKS HTML

JSON/template property: external_links

Example values: `<li class="external-link">KMUW: <strong><a href="http://kmuw.org/post/book-review-great-reckoning-lyrical-whodunnit" target="_blank">Book Review: 'A Great Reckoning' Is A Lyrical Whodunnit</a></strong></li>`

This property is optional.

### Internal fields

These fields are used for project management purposes and are not output as JSON or rendered to the end user.

#### EDITOR (internal use)

Example values: `Beth`

#### COST

Example values: `0`, `40`

#### GENRE

JSON/template property: genre

Example values: `Fiction`

This property is optional.

#### Assigned (1=yes)


#### Author Diversity (1=yes, 0=no)

Example values: `0`, `1`

###	REVIEWER DIVERSITY (1=yes, 0=no)

#### CONTACTED?

Example values: ``, `1`


### Unused fields

These fields didn't seem to be filled out for any of the book rows in the 2016 spreadsheet.

#### asin

#### oclc

#### genre (internal use)

#### fact-checking notes

#### Gender (1=woman, 0=man)


Bootstrap the project
---------------------

Node.js is required for the static asset pipeline. If you don't already have it, get it like this:

```
brew install node
curl https://npmjs.org/install.sh | sh
```

Then bootstrap the project:

```
cd books17
mkvirtualenv --no-site-packages books17
pip install -r requirements.txt
npm install
```

**Problems installing requirements?** You may need to run the pip command as ``ARCHFLAGS=-Wno-error=unused-command-line-argument-hard-error-in-future pip install -r requirements.txt`` to work around an issue with OSX.

Next, we will download and parse the text used for copy editing. If we don't do this, subsequent update commands fail:

```
fab text.update
```

After that we will need to download and parse our book list and covers:

```
fab data.update
```

_Note: The `DATA_GOOGLE\_DOC\_KEY` spreadsheet pointed in `app\_config.py` has to be published as a csv in order for the above command to work_

_Note: In order for cover images to be loaded, each book record has to have an ISBN value.  The books team enters this data, but doesn't get to it until later in the process.  If you want to test out the rig, you'll probably want to make a test version of the spreadsheet that includes more complete data, including ISBNs.  You can specify the test spreadsheet key by overriding the value of `DATA\_GOOGLE\_DOC\_KEY` in a `local\_settings` module._

Once that has been run, then we can do a full update that will sync also fonts & copy:

```
fab update
```

Hide project secrets
--------------------

Project secrets should **never** be stored in ``app_config.py`` or anywhere else in the repository. They will be leaked to the client if you do. Instead, always store passwords, keys, etc. in environment variables and document that they are needed here in the README.

Save media assets
-----------------

Large media assets (images, videos, audio) are synced with an Amazon S3 bucket specified in ``app_config.ASSETS_S3_BUCKET`` in a folder with the name of the project. (This bucket should not be the same as any of your ``app_config.PRODUCTION_S3_BUCKETS`` or ``app_config.STAGING_S3_BUCKETS``.) This allows everyone who works on the project to access these assets without storing them in the repo, giving us faster clone times and the ability to open source our work.

Syncing these assets requires running a couple different commands at the right times. When you create new assets or make changes to current assets that need to get uploaded to the server, run ```fab assets.sync```. This will do a few things:

* If there is an asset on S3 that does not exist on your local filesystem it will be downloaded.
* If there is an asset on that exists on your local filesystem but not on S3, you will be prompted to either upload (type "u") OR delete (type "d") your local copy.
* You can also upload all local files (type "la") or delete all local files (type "da"). Type "c" to cancel if you aren't sure what to do.
* If both you and the server have an asset and they are the same, it will be skipped.
* If both you and the server have an asset and they are different, you will be prompted to take either the remote version (type "r") or the local version (type "l").
* You can also take all remote versions (type "ra") or all local versions (type "la"). Type "c" to cancel if you aren't sure what to do.

Unfortunantely, there is no automatic way to know when a file has been intentionally deleted from the server or your local directory. When you want to simultaneously remove a file from the server and your local environment (i.e. it is not needed in the project any longer), run ```fab assets.rm:"www/assets/file_name_here.jpg"```

Adding a page to the site
-------------------------

A site can have any number of rendered pages, each with a corresponding template and view. To create a new one:

* Add a template to the ``templates`` directory. Ensure it extends ``_base.html``.
* Add a corresponding view function to ``app.py``. Decorate it with a route to the page name, i.e. ``@app.route('/filename.html')``
* By convention only views that end with ``.html`` and do not start with ``_``  will automatically be rendered when you call ``fab render``.

Run the project
---------------

A flask app is used to run the project locally. It will automatically recompile templates and assets on demand.

```
workon books17
fab app
```

Visit [localhost:8000](http://localhost:8000) in your browser.

COPY configuration
------------------

This app uses a Google Spreadsheet for a simple key/value store that provides an editing workflow.

To access the Google doc, you'll need to create a Google API project via the [Google developer console](http://console.developers.google.com).

Enable the Drive API for your project and create a "web application" client ID.

For the redirect URIs use:

* `http://localhost:8000/authenticate/`
* `http://127.0.0.1:8000/authenticate`
* `http://localhost:8888/authenticate/`
* `http://127.0.0.1:8888/authenticate`

For the Javascript origins use:

* `http://localhost:8000`
* `http://127.0.0.1:8000`
* `http://localhost:8888`
* `http://127.0.0.1:8888`

You'll also need to set some environment variables:

```
export GOOGLE_OAUTH_CLIENT_ID="something-something.apps.googleusercontent.com"
export GOOGLE_OAUTH_CONSUMER_SECRET="bIgLonGStringOfCharacT3rs"
export AUTHOMATIC_SALT="jAmOnYourKeyBoaRd"
```

Note that `AUTHOMATIC_SALT` can be set to any random string. It's just cryptographic salt for the authentication library we use.

Once set up, run `fab app` and visit `http://localhost:8000` in your browser. If authentication is not configured, you'll be asked to allow the application for read-only access to Google drive, the account profile, and offline access on behalf of one of your Google accounts. This should be a one-time operation across all app-template projects.

It is possible to grant access to other accounts on a per-project basis by changing `GOOGLE_OAUTH_CREDENTIALS_PATH` in `app_config.py`.

COPY editing
------------

This app uses a Google Spreadsheet for a simple key/value store that provides an editing workflow.

View the [sample copy spreadsheet](https://docs.google.com/spreadsheet/pub?key=0AlXMOHKxzQVRdHZuX1UycXplRlBfLVB0UVNldHJYZmc#gid=0).

This document is specified in ``app_config`` with the variable ``COPY_GOOGLE_DOC_KEY``. To use your own spreadsheet, change this value to reflect your document's key (found in the Google Docs URL after ``&key=``).

A few things to note:

* If there is a column called ``key``, there is expected to be a column called ``value`` and rows will be accessed in templates as key/value pairs
* Rows may also be accessed in templates by row index using iterators (see below)
* You may have any number of worksheets
* This document must be "published to the web" using Google Docs' interface

The app template is outfitted with a few ``fab`` utility functions that make pulling changes and updating your local data easy.

To update the latest document, simply run:

```
fab text.update
```

Note: ``text.update`` runs automatically whenever ``fab render`` is called.

At the template level, Jinja maintains a ``COPY`` object that you can use to access your values in the templates. Using our example sheet, to use the ``byline`` key in ``templates/index.html``:

```
{{ COPY.attribution.byline }}
```

More generally, you can access anything defined in your Google Doc like so:

```
{{ COPY.sheet_name.key_name }}
```

You may also access rows using iterators. In this case, the column headers of the spreadsheet become keys and the row cells values. For example:

```
{% for row in COPY.sheet_name %}
{{ row.column_one_header }}
{{ row.column_two_header }}
{% endfor %}
```

When naming keys in the COPY document, pleaseattempt to group them by common prefixes and order them by appearance on the page. For instance:

```
title
byline
about_header
about_body
about_url
download_label
download_url
```

Load books and covers
---------------------

To run the app, you'll need to load books and covers from a Google Spreadsheet.
First, see `DATA_GOOGLE_DOC_KEY` in `app_config.py`.

View a [sample data spreadsheet](https://docs.google.com/spreadsheets/d/10XgwGi631PgWrKwMp_OcFnVa7m4v9LXfwTDB5aXNUDw/edit?usp=sharing)


In order to get the covers for our books we are using an external service from BAKER & TAYLOR, in order to use it you will need your own credentials stored in these environment variables.

```
books17_BAKER_TAYLOR_USERID="SampleUser"
books17_BAKER_TAYLOR_PASSWORD="SamplePassword"
```

Then run the loader:

```
fab data.load_books
fab data.load_images
```

Alternatively, you can update copy and social media along with books with a
single command:

```
fab update
```

Get iTunes IDs
--------------

To create links that allow users to purchase books in the iTunes store, we need to add IDs to the `itunes_id` column of the books spreadsheet.  There is a Fabric task, `data.get_books_itunes_ids` that you can run to output a CSV from which you can copy and paste the IDs into the Books Google Spreadsheet.

There are however, a few caveats that are important to keep in mind.

This command takes a long time to run in order to get around the rate limiting of the iTunes search API.  It's probably best to run it first thing in the morning or to let it run overnight.

You'll want to make sure you update the book data before running this command.  Otherwise, the rows won't line up when you copy and paste into the Google Spreadsheet.  For the same reason, you will want to run the command when the book list is in a pretty stable state.

Now that you know the caveats, here's the task:

```
fab data.get_books_itunes_ids
```

By default, the command will read the books from `data/books.csv` and output the resulting iTunes IDs to `data/itunes_ids.csv`, but you can override either path:

```
fab data.get_books_itunes_ids:input_filename=data/new_books.csv,output_filename=data/new_books_itunes_ids.csv
```

This might be useful if you wanted to only get IDs for a subset of books that were added to the spreadsheet after the last time you fetched IDs.

If you need to get an iTunes ID for a single book, you can use the `data.get_book_itunes_id` task.

```
fab data.get_book_itunes_id:"The Apparitionists"
```

Get Goodreads IDs
-----------------

*NEW FOR 2017*

To generate links that allow users to access a book's Goodreads page, we need to get the Goodreads slug for each book. To get these slugs, you can run the Fabric task `data.get_books_goodreads_ids`, which will output a CSV from which you can copy and paste the slug into the `goodreads_id` column of the Books Google Spreadsheet.

There are a couple of caveats when running this command.

This command takes around 15-20 minutes to bypass the rate limiting of the Goodreads search API.  It's probably best to run it first thing in the morning or to let it run overnight.

You'll want to make sure you update the book data before running this command.  Otherwise, the rows won't line up when you copy and paste into the Google Spreadsheet.  For the same reason, you will want to run the command when the book list is in a pretty stable state.

To use the Goodreads API, you need a developer key. You should set this key as an environment variable like so: `books17_GOODREADS_API_KEY=YOUR_KEY_HERE` . If you need to replace this key, it's fairly simple to generate a new one from the [Goodreads API page](https://www.goodreads.com/api).

Here's the task:

```
fab data.get_books_goodreads_ids
```

By default, the command will read the books from `data/books.csv` and output the resulting iTunes IDs to `data/goodreads_ids.csv`, but you can override either path:

```
fab data.get_books_goodreads_ids:input_filename=data/new_books.csv,output_filename=data/new_books_goodreads_ids.csv
```

This might be useful if you wanted to only get the Goodreads slugs for a subset of books that were added to the spreadsheet after the last time you fetched them.

If you need to get a Goodreads ID for a single book, you can use the `data.get_book_goodreads_id` task.  Note that the argument to the task is the book's ISBN.

```
fab data.get_book_goodreads_id:0544745973
```

Get Links to Member Station Coverage
------------------------------------

*NEW FOR 2017*

The Books team tries to surface member station coverage of books. This content is pulled from a comma-separated list of HTML links (i.e. `<a>` tags) in the `EXTERNAL LINKS HTML`.

In 2017, the Books time decided to send a [Google Form](https://docs.google.com/forms/d/11VfB7WeBIg1YQKNzfVzbU5rae53PJ02d4Xm4e9yIajA/edit) to member stations soliciting their book coverage.  They asked for ISBNs to make it easier to programatically merge the station content with the books spreadsheet.

After the submissions close, Books editors copy the links and station information for coverage they want to include in the concierge into a [separate spreadsheet](https://docs.google.com/spreadsheets/d/16Zt1Zs5bghJrZ_5oCS04UUXrk_WrRTjGGs9IbZw5ogM/edit)

You'll also need to publish this spreadsheet to the web as CSV.

Then, you can run:

```
fab data.update
fab data.load_station_coverage_headlines
```

to create a CSV file that contains headlines for the station coverage that can be copied and pasted back into the Google spreadsheet for editing.  This CSV file is `data/station_coverage_headlines.csv`.

Since we get the headlines by requesting and parsing the HTML, this command can take a few minutes to run.

As we're pulling headlines of the coverage from the pages' `<title>` tag, you'll probably want to edit the headline text after you copy them into the Google sheet.

Once headlines have been populated and edited, you can run:

```
fab data.update
fab data.load_external_links
```

This Fabric task does a few things.  First, it downloads the station coverage Google spreadsheet as CSV to `data/station_coverage.csv`. It then generates HTML links for the station coverage and builds a lookup table by ISBN and stores that as JSON in `data/external_links_by_isbn.json`.  Finally, it merges the books in the book list with the external links and outputs a CSV file in `data/external_links_to_merge.csv`.

The values in `data/external_links_to_merge.csv` can be copied and pasted into the books Google spreadsheet.  Because the order of rows in the CSV file follows the books spreadsheet, it makes sense to run this command after the book list is very stable.  Also, be sure that the local CSV of the book list is up-to-date by running `fab data.update`.

I had some issues with row mismatches when copying and pasting the generated external links column out of Excel and into the books Google sheet. I had much better luck just importing the CSV as a new worksheet into the Google spreadsheet and copying and pasting into the books worksheet.


Arbitrary Google Docs
----------------------
Sometimes, our projects need to read data from a Google Doc that's not involved with the COPY rig. In this case, we've got a class for you to download and parse an arbitrary Google Doc to a CSV.

This solution will download the uncached version of the document, unlike those methods which use the "publish to the Web" functionality baked into Google Docs. Published versions can take up to 15 minutes up update!

First, export a valid Google username (email address) and password to your environment.

```
export APPS_GOOGLE_EMAIL=foo@gmail.com
export APPS_GOOGLE_PASS=MyPaSsW0rd1!
```

Then, you can load up the `GoogleDoc` class in `etc/gdocs.py` to handle the task of authenticating and downloading your Google Doc.

Here's an example of what you might do:

```
import csv

from etc.gdoc import GoogleDoc

def read_my_google_doc():
    doc = {}
    doc['key'] = '0ArVJ2rZZnZpDdEFxUlY5eDBDN1NCSG55ZXNvTnlyWnc'
    doc['gid'] = '4'
    doc['file_format'] = 'csv'
    doc['file_name'] = 'gdoc_%s.%s' % (doc['key'], doc['file_format'])

    g = GoogleDoc(**doc)
    g.get_auth()
    g.get_document()

    with open('data/%s' % doc['file_name'], 'wb') as readfile:
        csv_file = list(csv.DictReader(readfile))

    for line_number, row in enumerate(csv_file):
        print line_number, row

read_my_google_doc()
```

Google documents will be downloaded to `data/gdoc.csv` by default.

You can pass the class many keyword arguments if you'd like; here's what you can change:
* gid AKA the sheet number
* key AKA the Google Docs document ID
* file_format (xlsx, csv, json)
* file_name (to download to)

See `etc/gdocs.py` for more documentation.

Run Python tests
----------------

Python unit tests are stored in the ``tests`` directory. Run them with ``fab tests``.

Run Javascript tests
--------------------

With the project running, visit [localhost:8000/test/SpecRunner.html](http://localhost:8000/test/SpecRunner.html).

Compile static assets
---------------------

Compile LESS to CSS, compile javascript templates to Javascript and minify all assets:

```
workon books17
fab render
```

(This is done automatically whenever you deploy to S3.)

Test the rendered app
---------------------

If you want to test the app once you've rendered it out, just use the Python webserver:

```
cd www
python -m SimpleHTTPServer
```

Deploy to S3
------------

```
fab staging deploy
```

If you have already loaded books and cover images, you can skip this time-consuming step when
deploying by running:

```
fab staging deploy:quick
```


Analytics
---------

The Google Analytics events tracked in this application are:

|Category|Action|Label|Value|Notes|
|--------|------|-----|-----|-----|
|best-books-2017|tweet|`location`|||
|best-books-2017|facebook|`location`|||
|best-books-2017|pinterest|`location`|||
|best-books-2017|email|`location`|||
|best-books-2017|open-share-discuss|||
|best-books-2017|close-share-discuss|||
|best-books-2017|summary-copied|||
|best-books-2017|view-review|`book_slug`|||
|best-books-2017|navigate|`next` or `previous`|||
|best-books-2017|toggle-view|`list` or `grid`|||
|best-books-2017|clear-tags||||
|best-books-2017|selected-tags|`comma separated list of tags`|||
|best-books-2017|library|`book_slug`||Book slug of library click|
|best-books-2017|amazon|`book_slug`||Book slug of amazon click|
|best-books-2017|ibooks|`book_slug`||Book slug of ibooks click|
|best-books-2017|indiebound|`book_slug`||Book slug of indiebound click|
