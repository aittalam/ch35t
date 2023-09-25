# ch35t

## signature

## label

### name
### URI
### author

## hint

### origin
A reference to the data (eg. URL)

### data
The actual data (typically a string which is base64 encoded).
Data format is inspired to data URLs, i.e. 
```
data:[mime-type][;base64],<data>
```
But here is just
```
[base64],<data>
```
Data is not URI-encoded

### format
The format of the data / origin. Define which action to take with the data, depending on the associated handler.
Format is, by default, `text/plain`

## payload

### origin
### data
### format
### method
NOTE: make it into Name + params, not just a plain string
### output-format 
What is the format of the decrypted output?

—-
- JSON from file, URL, string
- 