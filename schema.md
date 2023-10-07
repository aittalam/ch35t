# Ch35t Schema

*Chests as defined in the Ch35t format*

## Properties

- **`label`** *(object)*: A label attached to the chest, containing information about it. Cannot contain additional properties.
  - **`name`** *(string, required)*: The chest name.
  - **`URI`** *(string, format: uri)*: A Uniform Resource Identifier for the chest (can match the URL it can be downloaded from.
  - **`author`** *(string, format: email)*: The email address of the chest creator (often used in conjuction with a signature.
- **`hint`** *(object)*: A hint that might help you find the key to open the chest. Cannot contain additional properties.
  - **`origin`** *(string, format: uri)*: A Uniform Resource Identifier for the hint (can match the URL it can be downloaded from).
  - **`data`** *(string)*: The hint contents (plain text or base64-encoded binary).
  - **`format`**: The format (mime-type) of the hint contents. Note that we currently allow only formats for which we have a handler, but this is not strictly necessary (i.e. we can just save files we do not know how to handle and allow players to deal with them). Must be one of: `["text/plain", "application/zip"]`.
- **`payload`** *(object)*: Cannot contain additional properties.
  - **`origin`** *(string, format: uri)*: A Uniform Resource Identifier for the payload (can match the URL it can be downloaded from).
  - **`data`** *(string)*: The hint contents (plain text or base64-encoded binary).
  - **`format`**: The format (mime-type) of the payload contents. Note that we currently allow only formats for which we have a handler, but this is not strictly necessary (i.e. we can just save files we do not know how to handle and allow players to deal with them). Must be one of: `["text/plain", "application/zip"]`.
  - **`output-format`** *(string)*: The format (mime-type) of the decrypted payload. Note that as we do not necessarily need to handle this, we leave the possibility of using any format here.
  - **`method`** *(object)*: The encryption method used to conceal the payload. Cannot contain additional properties.
    - **`name`** *(string, required)*: The name of the encryption method.
    - **`args`** *(array)*: Extra arguments to be provided to the method handler.
      - **Items** *(string)*
- **`signature`** *(string)*
