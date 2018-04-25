## Proof of Freshness
This is just to demonstrate different ways to prove freshness when making documents or files. This is great for cryptographic applications (take the hash of the webpage) and verifying that a document was not made before a certain date.

## Using in other applications
If you need a proof of freshness or think it might be useful, just include all or some data from [homelabs.space:2052/pof](http://homelabs.space:2052/pof). Then, anyone will be able to verify the freshness of your document through the headlines from major reputable newspapers, latest bitcoin hash, and NIST's randomness beacon. You can copy and paste or use curl to grab the latest proofs of freshness.

```
curl homelabs.space:2052/pof
```

## Running
```bash
export FLASK_APP=app.py
flask run
```

## Running using Docker
```bash
docker build . -t pof_flask && docker run --name pof_flask -p 8000:8000 pof_flask
```

Notes:
- You might need to use `sudo` for Docker to work.

Proof of freshness demo (using docker): [homelabs.space:2052/pof](http://homelabs.space:2052/pof)

## Uses
- Preventing warrant canaries from being created in advance
- Narrowing the window where documents can be signed (in conjunction with [opentimestamps])
- Sources of randomness (useful for Multi-party Computation and zero knowledge proofs)
- Establishing trust (its easy to include a proof of freshness and leaving it out might imply that you can't)

If you come up with any other use for a proof of freshness, just open up an issue.

## Contributions and other possible sources
Other sources I would like to add include:
- Congress's votes (would cause big political fuss if anybody wanted to interfere) using [ProPublica's API](https://projects.propublica.org/api-docs/congress-api/votes/) ProPublica also has some other awesome datasets which may be useful
- World and national stocks
- Other cryptocurrencies (especially privacy-centric ones)
- Foreign sources (I don't really know any reputable newspapers outside of the US)

## Other ideas for this project
- Create an API or json way to make it easier to intergrate with other applications

Contributions are always welcome!
