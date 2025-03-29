---
title: How did I created my website?
updated: 2024-01-27 19:43:12Z
date: 2023-12-19 20:08:14Z
tags: ["Hugo", "Website"]
---

{{< warning "Info" >}}
This post is outdated, I do not use the theme specified in this post anymore.
{{< /warning >}}

This post primarily serves as documentation for my website. Additionally, if someone finds something useful here, they are welcome to use it. The entire source code, including blog posts and their digital signatures, can be found on [GitHub](https://github.com/MonkeManX/monkemanx.github.io).

I created my website using three main components:
- **Server Host:** I utilize [Github-Pages](https://pages.github.com/) for hosting. I choose GitHub Pages, because they are free and it's really easy to upload files to it.
- **Website Framework:** The website is built using [Hugo](https://gohugo.io/), a static website generator. Hugo can generate a website from markdown files, making it really easy to add new content to the website.
- **Website-Theme:** I choose the [PaperMod](https://github.com/adityatelange/hugo-PaperMod) theme for my Website. Hugo offers all kinds of different [themes](https://github.com/topics/hugo-theme) one can use, I choose PaperMod since its simple and I like its look.

One important disclaimer for those considering GitHub Pages: the repository must be public. If you prefer to use GitHub Pages with a private repository, you will need either GitHub Pro or Enterprise.

# Installing Hugo

For a detailed guide on how to install Hugo, I recommend visiting the [official Hugo website](https://gohugo.io/installation/). If you have at any point difficulties installing Hugo, refer to that website for assistance.

On Debian and Debian-based Operating System, such as Ubuntu, you can install Hugo using the `apt` package manager. Open a terminal and type the following:
```sh
sudo apt install hugo`
```
To verify the installed version of Hugo, you can use the following command:
```sh
hugo version
```
Keep in mind Debian, has a very slow release cycle. In my case, the installed version was not up-to-date, so I chose to uninstall it:
```sh
sudo apt remove hugo
```
Instead, I installed the latest Hugo version, by downloading the package directly from [GitHub]( https://github.com/gohugoio/hugo/releases ).

For Windows users, Hugo can be installed using a package manager like *[choco](https://chocolatey.org/),* *scoop* or *winget*.
For instance, to install Hugo via chocolate execute the following command: 
```sh
choco install hugo-extended
```

# Creating a Project

To start your Hugo project, you can refer to the [Hugo quickstart guide](https://gohugo.io/getting-started/quick-start/) for guidance.

We begin by establishing the folder structure for your Hugo project. Open a terminal in the desired folder for your project and create a new Hugo project with the following command:
```sh
hugo new site <website_folder_name> --format yaml
```
I recommend including the `--format yaml` argument when creating the project.
This ensures that the project configuration file is generated using a YAML format, which in my opinion, is more readable. However if you omit the `--format yaml` argument, the configuration file will be generated in the `.toml` format.

# Installing the Theme

Themes play a crucial role in determining the front-end design, overall appearance, and functionality of your website. They provide a collection of site layouts that make it easy to build a website. Numerous Hugo themes can be found on [GitHub](https://github.com/topics/hugo-theme).

For my website, I choose the [PaperMod](https://github.com/adityatelange/hugo-PaperMod) theme which features a clean modern design:

{{< rawhtml >}}
<figure>
    <img loading="lazy" style="display: block; margin-left: auto; margin-right: auto; width:100%" src="/attachments/114303440-bfc0ae80-9aeb-11eb-8cfa-48a4bb385a6d.png">
    <figcaption style="text-align:center"><a href="https://github.com/adityatelange/hugo-PaperMod">Source</a></figcaption>
</figure>
{{< /rawhtml >}}

To install the PaperMod theme and ensure compatibility with GitHub Pages, use the [second installation method](https://github.com/adityatelange/hugo-PaperMod/wiki/Installation), which involves using git sub modules:
```
git submodule add --depth=1 https://github.com/adityatelange/hugo-PaperMod.git themes/PaperMod
git submodule update --init --recursive
```
If in the future you need to re clone your repository, remember to execute the second command again, s the submodule might not be included in the cloning process.

To update the theme, use the following command:
```sh
git submodule update --remote --merge
```

After installing the theme, you need to inform Hugo that you want to use the PaperMod theme. To do that, you need to edit the `hugo.yaml` file and add the following line:
```yaml
theme: "PaperMod"
```

# The Project Structure

After creating your project structure and installing a theme of your choice, your project structure should resemble the following:

```sh
├───archetypes
├───assets
├───content
├───data
├───i18n
├───layouts
├───public
├───static
├───themes
└───hugo.yml
```

Key components of this structure include:
- `content`: This folder is used to store the content of your website. In here you save your markdown files, which will be used to generate the site.
- `public`: Hugo saves the built websites in this folder. It contains the final output of your website that can be deployed.
- `static`: This folder is used to store static data such as images or videos for your pages.
- `themes`: Here, the installed theme is saved. If you want to customize the appearance or behavior of the theme, you would make modifications in this folder.
- `hugo.yml`:  This file is the general configuration file for your website. You can adjust various settings, such as the title of your website or the author information.

For more thorough explanation, refer to the Hugo website [guide on directory structure](https://gohugo.io/getting-started/directory-structure/).

#  Configure Settings

## General Settings

To tailor the behavior and appearance of your website, edit the `hugo.yml` file within the project structure. All changes mentioned in this section will be made in that file unless specified otherwise. If you chose a different format during installation, the file name could be either `hugo.toml` or `hugo.json`.

The first modification addresses privacy settings to align with [GDPR](https://en.wikipedia.org/wiki/General_Data_Protection_Regulation) guidelines: 
```yml
privacy:
  disqus:
    disable: true
  googleAnalytics:
    disable: true
  instagram:
    disable: true
  twitter:
    disable: true
  vimeo:
    disable: true
  youtube:
    disable: true
```

For enhanced website security, I use the following HTTP headers configurations:
```sh
server:
  headers:
  - for: /**
    values:
      Content-Security-Policy: script-src localhost:1313
      Referrer-Policy: strict-origin-when-cross-origin
      X-Content-Type-Options: nosniff
      X-Frame-Options: DENY
      X-XSS-Protection: 1; mode=block
```
For a more in depth guide on what these different configurations mean you can check out the awesome [cheat-sheet from owsap](https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html) on this topic.
Another useful tool in combination with that is the following website: [security-header](https://securityheaders.com/?q=https%3A%2F%2Fmonkemanx.github.io%2F&followRedirects=on) which allows you to check if the HTTP headers of your website are really correctly configured.

## Params Settings

The following section is about the `params` section of the configuration file. If the `params` section doesn't exist, create it in the configuration file. Refer to my complete `hugo.yml` file for more details.

Here are some other neat settings I found, some of them are from Hugo others are from my theme:
- `howReadingTime: true`:  Provides an estimate of how long it would take to read each post.
- `ShowCodeCopyButtons: true`:  Allows copying of code from code blocks with a button press.
- `ShowWordCount: true`:  Displays the number of words at the top of each post.
- `ShowRssButtonInSectionTermList: true`:  Adds an RSS icon to the archive page.

Refer to the [PapersMod variables](https://github.com/adityatelange/hugo-PaperMod/wiki/Variables) for additional settings.

## Menu

Finally, I adjusted the website menu by modifying the menu section. The example below illustrates the menu:

{{< rawhtml >}}
<figure>
    <img loading="lazy" style="display: block; margin-left: auto; margin-right: auto; width:80%" src="/attachments/2023-12-21_22-50.png">
</figure>
{{< /rawhtml >}}

To archive a menu like shown above, the first thing you need to do is add the following to the `hugo.yaml`:
```yml
menu:
  main:
    - identifier: home
      name: Home
      url: /posts/
      weight: 10
    - identifier: about
      name: About
      url: /about
      weight: 20
    - identifier: tags
      name: Posts by Tags
      url: /tags/
      weight: 30
    - identifier: archive
      name: Archive
      url: archives
      weight: 40
```
The `identifier` is a unique name for every item in the menu, the `url` describes the location the link in the menu leads to, keep in mind the URLs starts implicit already in the `content` folder.
The weight `describes` the physical location of the menu, with it you can order the menus into a custom order.

The `home`  button leads back to the homepage, which shows an overview of my recent blog posts:

{{< rawhtml >}}
<figure>
    <img loading="lazy" style="display: block; margin-left: auto; margin-right: auto; width:80%" src="/attachments/Screenshot%20from%202023-12-21%2022-58-11.png">
</figure>
{{< /rawhtml >}}

The `About` button leads to a site, which describes what the website is about, this page is also not visible in the archive or on the homepage:

{{< rawhtml >}}
<figure>
    <img loading="lazy" style="display: block; margin-left: auto; margin-right: auto; width:80%" src="/attachments/Screenshot%20from%202023-12-21%2022-58-29.png">
</figure>
{{< /rawhtml >}}

The `tags` button leads to a site, where one can search for posts by tags:

{{< rawhtml >}}
<figure>
    <img loading="lazy" style="display: block; margin-left: auto; margin-right: auto; width:80%" src="/attachments/Screenshot%20from%202023-12-21%2022-58-49.png">
</figure>
{{< /rawhtml >}}

The `Archive` button leads to a site, which depicts all posted posts by time they were posted, you can see here an example:

{{< rawhtml >}}
<figure>
    <img loading="lazy" style="display: block; margin-left: auto; margin-right: auto; width:80%" src="/attachments/Screenshot%20from%202023-12-21%2022-59-02.png">
</figure>
{{< /rawhtml >}}

For the archive site to work properly, you need to create a `archives.md` file in the `content` folder, with the following lines in it:
```md
+++
title = "Archive"
layout = "archives"
url = "/archives/"
summary = "archives"
+++
```
Everything between the pluses is called [front matter](https://gohugo.io/content-management/front-matter/) and is used to embed meta information about the file.

## Summary

In summary my complete `hugo.yml` file is the following:
{{< details "Click here to show it" >}}
```yml
baseURL: ''
title: Title-of-Website
languageCode: en-us
theme: "PaperMod"

privacy:
  disqus:
    disable: true
  googleAnalytics:
    disable: true
  instagram:
    disable: true
  twitter:
    disable: true
  vimeo:
    disable: true
  youtube:
    disable: true

server:
  headers:
  - for: /**
    values:
      Content-Security-Policy: script-src localhost:1313
      Referrer-Policy: strict-origin-when-cross-origin
      X-Content-Type-Options: nosniff
      X-Frame-Options: DENY
      X-XSS-Protection: 1; mode=block

params:
  name: MonkeMan
  email: WiseServiceScholar@protonmail.com
  ShowRssButtonInSectionTermList: true
  description: The Personel Blog of MonkeMan
  keyword: ["blog"]
  ShowReadingTime: true
  ShowShareButtons: false
  ShowWordCount: true
  ShowCodeCopyButtons: true
  
menu:
  main:
    - identifier: home
      name: Home
      url: /posts/
      weight: 10
    - identifier: about
      name: About
      url: /about
      weight: 20
    - identifier: tags
      name: Posts by Tags
      url: /tags/
      weight: 30
    - identifier: archive
      name: Archive
      url: archives
      weight: 40
    
```
{{< /details >}}

# Adding Content to Your Website

Adding content to your website involves creating new pages, blog posts, or sections. As demonstrated in the previous section, you can include these in the menu by updating the `hugo.yml` file.

To add an About page to the menu, execute the following command:
```sh
hugo new about.md
```
Remember to be in the project folder when running this command. The file will be created in the content directory. Edit the `about.md` file to add content to the About page. For example:
```md
+++
title = 'About'
date = 2023-12-21T20:00:07+01:00
draft = true
hiddenInHomelist = true
+++
# About

I am a very cool guy!
```

To create a new blog post visible on the homepage and in the archive, use the command:
```sh
hugo new posts/new-cool-post.md
```
This will create a markdown file `new-cool-post.md`, in the `content/posts` folder.

To make blog posts discoverable by tags, you can include tags in the front matter of the post. Like this:
```
+++
tags = ["my-first-cool-tag", "my-second-cool-tag"]
+++
```

To add an image to a page, place the image in the static folder and reference it in the markdown file:
```
![name_of_image](/name_of_image.png)
```

In the `frontmatter` of your markdown file you can change a bunch of setting on how the post will appear. Some useful settings include:
- `tags`, If you want that your blog post are discoverable by tags
- `hiddenInHomelist`, If you want to hide some blog post
- `drafts`, set this to false for deployment, hugo doesn't build draft files to html sites.

Refer to [PaperMod Variables](https://github.com/adityatelange/hugo-PaperMod/wiki/Variables) for more front matter settings.

When ready to build your site, run:
```sh
hugo serve
```
To include drafts in the build, add the `--buildDrafts` option. 
Hugo will spin up a webserver hosting your website, you can access it through `localhost:1313`.

## Shortcodes

Shortcodes in Hugo are like custom tags that you can use to extend the functionality of your content. They allow you to embed dynamic elements or execute custom logic within your markdown files.

### Details Shortcode

In my case, I wanted a shortcode named `details` to generate foldable markdown boxes. Like this:
I wanted a shortcode which would allow me to use foldable markdown box:

{{< rawhtml >}}
<figure>
    <img loading="lazy" style="display: block; margin-left: auto; margin-right: auto; width:60%" src="/attachments/Screenshot%20from%202023-12-23%2017-33-45.png">
</figure>
{{< /rawhtml >}}

Here's a brief explanation of how it works:
1. Shortcodes are stored in the `/layouts/shortcodes/` directory. The shortcode file, `details.html`, contains HTML and Hugo templating code. 
2. Shortcodes can take parameters to customize their behavior. In the details shortcode, we use a parameters: `$summary` for the summary text.
3. To use the `details` shortcode, you include it in your markdown content with `\{\{< details ... >\}\}`(without the backslashes).

{{< details "The full `details.html` code" >}}
```html
<style>
  /* Style for the details element */
  details {
    border: 2px solid #3498db; /* Change border color to a noticeable color, e.g., blue */
    border-radius: 8px;
    margin: 20px 0;
    padding: 15px;
    background-color: #f2f2f2; /* Add a light background color */
    overflow: hidden; /* Hide the content initially */
    transition: max-height 0.5s ease-out; /* Add a transition effect */
    max-height: 70px; /* Set a max-height value to determine the collapsed height */
  }

  /* Style for the summary element */
  summary {
    font-weight: bold;
    cursor: pointer;
    color: #3498db; /* Match the border color for consistency */
  }

  /* Style for the content inside the details element */
  .collapsible-content {
    margin-top: 10px;
  }

  /* Expand the details when it's open */
  details[open] {
    max-height: 500px; /* Set a higher value for the expanded height */
  }
</style>

<details>
  <summary>{{ (.Get 0) | markdownify }}</summary>
  <div class="collapsible-content">
    {{ .Inner | markdownify }}
  </div>
</details>
```
{{< /details >}}

An usage example in a blog post(again without the backslashes):
```markdown
# This is my cool blog

I have a lot to say, look at this:

\{\{< details "This is the summary" >\}\}
Collapsed text
\{\{< /details >\}\}

And here I have more to say.
```

### Warning Shortcode

Another shortcode I added was the warnings shortcode this is basically a red box with title and some kind of content:
{{< details "The full `warning.html` code" >}}
```html
<!-- layouts/shortcodes/warning.html -->
<style>
    .warning {
        background-color: #ffe4e1; /* Light pink background color */
        padding: 15px; /* Padding inside the box */
        border-radius: 5px; /* Rounded corners */
        margin-bottom: 15px; /* Margin at the bottom for spacing */
    }

    .warning-title {
        font-size: 20px; /* Title font size */
        margin-bottom: 10px; /* Margin below the title */
        color: #8b0000; /* Dark red text color */
        font-weight: bold; /* Bold text */
    }
</style>

<div class="warning">
    <div class="warning-title">{{ .Get 0 | markdownify | safeHTML }}</div>
    <p>{{ .Inner}}</p>
</div>
```
{{< /details >}}

## Images and Adding Captions

In Hugo, adding captions to images can be achieved using custom render hooks. Here's a step-by-step guide:

1. Edit the file(or create it) named `render-image.html` in the /`themes/PaperMod/layouts/_default/_markup` directory. Add the following custom code:
    ```sh
    {{ if .Title }}
      <figure class="latex-figure">
        <img loading="lazy" src="{{ .Destination | safeURL }}" alt="{{ .Text }}">
        <figcaption>
            <p>{{ .Title | markdownify }}</p>
        </figcaption>
      </figure>
    {{ else }}
      <img loading="lazy" src="{{ .Destination | safeURL }}" alt="{{ .Text }}">
    {{ end }}
    ```
2. Now, when you add an image in your markdown, you can include a caption using the `![Alt Text](Image URL "Caption")` syntax. For example:
    ```markdown
    ![monke](/monke.jpg "test suopper cool caption")
    ``` 
    To add a image source to your Image:
    ```markdown
    ![monke](/monke.jpg "Test [source](https://google.com)")
    ``` 
3. If needed you can adjust the CSS styling in the `render-image.html` file.

## HTML Content and custom CSS

If you already have finished html files that you want to add to your blog, you can add them to your content folder liek your markdown files. In order for them to be dispalyed correctly you need to add a front-matter section:
```html
+++
title = 'Title'
date = 2023-12-22T00:32:40+01:00
draft = true
```

If you want to add some custom CSS code to **all** your sites/posts, you can do this by creating a `.css` file in the folder `assets/css/extended`, all the CSS code in this file will be applied to all pages.

If you want to add some custom CSS code to a **single** site, you can do this by creating a custom `.css` file in your `static` folder, after which you need to edit the `single.html` in the `themes/YOUR_THEME/layout/_default/` folder and add the following section to it:
```md
{{ with .Params.custom_css }}
  {{- $customCSSPath := printf "%s.css" . }}
  <link rel="stylesheet" href="{{ $customCSSPath | absURL }}">
{{ end }}
```
The last thing you need to do it to edit the front matter of the html file to which you want to apply your custom css:
```md
+++
title = 'title'
date = 2023-12-22T00:32:40+01:00
draft = true
custom_css = "your_custom_cdd"
+++
```

# Comments

Adding comments or guest books to static sites, especially those hosted on platforms like GitHub Pages, can be challenging due to the lack of server-side processing like the lack of PHP or databases. I looked at some different options:
1. **Self-Made Code:** Many traditional comment systems, like those using PHP, require server-side processing, which is not supported on GitHub Pages.
2. **External Hosting:** Some third-party services offer comment systems that work with static sites. Examples of this are Disquis or Commento. But such sites have often times privacy concerns

As such I didn't add any commenting feature to my website.

# Conclusion

I hope this quick tutorial could help whomever read this through their journey of hosting a website.
I will try to keep this post up to date with my changing website, but I might forget to.

---
References:
- https://sebastiandedeyne.com/captioned-images-with-markdown-render-hooks-in-hugo/
- https://gohugo.io/
- https://pages.github.com/
- https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html
- https://github.com/adityatelange/hugo-PaperMod
