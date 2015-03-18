# Abbots Morton Experiment

Abbots Morton Experiment is a sans-serif font for [Quikscript][qs] that uses contextual alternates to replicate proper Quikscript writing.

See it in action [on the blog at frogorbits.com][blog].


## Hacking

Glyph connection positions are described by their height:

- ‘t’ for Tall
- ‘s’ for Short
- ‘b’ for at the baseline
- ‘d’ for Deep

With this, we can describe a character’s connection capabilities in its suffix. Thus:

- may-qs is an isolate form, suitable for Junior Quikscript
- may-qs.b2 is a final form that connects to the previous letter at the baseline
- may-qs.2s is an initial form that connects to the next letter at the Short height
- may-qs.b2s is a medial form that starts at the baseline and connects to the Short height
- may-qs.s2b is another medial form that starts at the top of the letter and ends deep inside

The sorts of connections a letter is tuned for can be further described:

- ‘r’ for “reach” — utter-qs.2sr is designed to reach over to the Short connection at the top of .May

Incidentally, the sample string that Font Book uses can be changed by editing “the name ID=19 sample string”. Dunno if Glyphs can do that yet.

## License

Apache License, version 2.0.

[qs]: http://en.wikipedia.org/wiki/Quikscript
[blog]: https://www.frogorbits.com/blog/
