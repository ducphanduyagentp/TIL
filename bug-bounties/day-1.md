# Day 1

- Recon for subdomains
    - Scan all ports for services

## Yahoo
- Yahoo! Query Language console
- Not a lot of sinks. However, the attack surface is large and there are janky input filtering
    - Strip off any kind of tags in the profile names
    - HTML entities are displayed normally but things like quotes and slashes though

## Flickr
- A lot of sinks
- Attack surface is also large because there are a lot of places where assets can be created
- Allow some HTML in the description
- Also does weird input sanitization but seems like it's not really consistent

## Tools

- Need good tools to find sources and sinks of the application
    - tracy is pretty good but the output is large and does not cover all kinds of responses (!?)
    - look in to contributing to tracy
- Need to develop a short test payload to check for all kinds of filters/encoding.