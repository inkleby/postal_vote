###About

This website is a showcase for how data can be transformed through presentation. It takes the core dataset (the International Astronomical Union’s Gazetteer of Planetary Nomenclature) and combines it with other data to extrapolate information not apparent in any one source. 

Essentially it’s a demonstration of how a dataset can be transformed by highlighting connections and bringing context to the information. So there’s a crater at blah coordinates - but where is that? Can we see it on a map? What’s nearby? How long would it take to get somewhere else? It’s named after someone, but who is that person? Where can I found out more?

WNTS is a product of the following datasets:

* Gazetteer of Planetary Nomenclature
* Wikipedia data on space features
* Wikipedia biographical data
* Planetary nomenclature naming conventions
* Definitions of planetary features
* Maps of the Moon and Mars made available through Google Maps’ API.
* Maps of Mercury, Venus, and assorted Jovean and Saturnian moons - converted into custom tiles (sources at bottom of page).
* [LRO LOLA Elevation Model](http://astrogeology.usgs.gov/search/details/Moon/LRO/LOLA/Lunar_LRO_LOLA_Global_LDEM_118m_Mar2014/cub) (for moon rover).

Google Maps already supports maps of the Moon and Mars, for other planets and moons the world maps had to be converted into tilesets to support mapping. This makes this the first website where you can easily explore maps of so many bodies in the solar system in the same place. (Conversion code available [here](https://github.com/inkleby/google_maps_tile_converter), tilesets available [here](https://github.com/inkleby/world_tiles/tree/gh-pages)). 

The dataset adding the most value is Wikipedia - WNTS uses it in two ways: 

If the feature has been named after a person it will extract the person’s name and try and create a hyperlink to that person’s entry. This makes the previously fairly opaque ‘origin’ column in the gazetter a jumping off point to learn more. 

If the feature itself already has a wikipedia article (for instance most features on the Moon do) - it will extract the summary and try and boil that summary down to the most relevant information that isn’t repeating what the page already knows (e.g. who it’s named for), knocking out repeating words, taking out sentences flagged as dull, etc. This keeps the summary shorter and hopefully more focused on what is more ‘interesting’ information. Any other place names mentioned will becomes internal links - reintegrating the external text data with context from the local system. 

###Emergent data

When you gather sufficient information you can create new information that didn’t exist in any one source (connected databases are more useful than the sum of their parts).

For instance, by adding a database of planetary radiuses to the gazetteer we can treat their lat/long coordinates as points on a sphere and calculate great circle routes to find the distance between them. By knowing the strength of gravity on a world, we can calculate(ish) a value for walking speed - and say how long it will take to walk between two entries. This takes an otherwise quite abstract database and puts it a very old context - “it would take you two hours to walk there.”

Walking speed is calculated using the [Froude-number equation](http://www.nature.com/nature/journal/v409/n6819/fig_tab/409467a0_F1.html). When gravity becomes so low that walking would no longer be a viable strategy we stop trying to calculate it. 

###Turning the lens around

We can change how the data is presented to ask different questions of it. For instance, the IAU website tells us if a feature name comes from a particular culture - but doesn't make it to see the reverse. WNTS shows per world the sources of the names on it - and points out any that only appear on that world. 

###Automated storytelling

Like Pathfinder had Sojourner, this website has a little robot valiantly working its way round the moon in real time. Unlike [other Inkleby robots](http://www.inkleby.com/robots/), this one is taking a structured approach to the dataset - moving from one point to another at 20 kmph (give or take time given going up and down). 

The rover’s twitter feed tries to present a different view on the moon by showing the rover’s path side-on rather than top down - to get a feel for the elevation of the moon.

###Test of semi-static architecture

More of a technical point - what we call things in space don’t change that often so to have a typical django server running the site is wasteful. Baking the site into static pages makes it quicker to load - and also means you can take advantage of reduced hosting requirements. 

There are several things that are trivial to do on a server this approach makes difficult - for instance search and moving between ‘on path’ and ‘off path’ while exploring. This site tests out some methods for keeping the ‘dynamic’ parts of a site moving while taking away most of the moving parts.