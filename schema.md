# Ch35t Schema

*Chests as defined in the Ch35t format*

## Properties

- <a id="properties/label"></a>**`label`** *(object, required)*: A label attached to the chest, containing information about it. Cannot contain additional properties.
  - <a id="properties/label/properties/name"></a>**`name`** *(string, required)*: The chest name.
  - <a id="properties/label/properties/URI"></a>**`URI`** *(string, format: uri)*: A Uniform Resource Identifier for the chest (might correspond to the URL the riddle can be downloaded from).
  - <a id="properties/label/properties/author"></a>**`author`** *(string, format: email)*: The email address of the chest creator (often used in conjuction with a signature.
- <a id="properties/hint"></a>**`hint`** *(object)*: A hint that might help you find the key to open the chest. Cannot contain additional properties.
  - <a id="properties/hint/properties/origin"></a>**`origin`** *(string, format: uri)*: A Uniform Resource Identifier for the hint (might correspond to the URL the hint can be downloaded from).
  - <a id="properties/hint/properties/data"></a>**`data`** *(string)*: The hint contents (plain text or base64-encoded binary).
  - <a id="properties/hint/properties/format"></a>**`format`**: The format (mime-type) of the hint contents. Note that we currently allow only formats for which we have a handler, but this is not strictly necessary (i.e. we can just save files we do not know how to handle and allow players to deal with them). Must be one of: "text/plain" or "application/zip".
- <a id="properties/payload"></a>**`payload`** *(object, required)*: Cannot contain additional properties.
  - <a id="properties/payload/properties/origin"></a>**`origin`** *(string, format: uri)*: A Uniform Resource Identifier for the payload (might correspond to the URL the payload can be downloaded from).
  - <a id="properties/payload/properties/data"></a>**`data`** *(string)*: The hint contents (plain text or base64-encoded binary).
  - <a id="properties/payload/properties/format"></a>**`format`**: The format (mime-type) of the payload contents. Note that we currently allow only formats for which we have a handler, but this is not strictly necessary (i.e. we can just save files we do not know how to handle and allow players to deal with them). Must be one of: "text/plain" or "application/zip".
  - <a id="properties/payload/properties/output-format"></a>**`output-format`** *(string)*: The format (mime-type) of the decrypted payload. Note that as we do not necessarily need to handle this, we leave the possibility of using any format here.
  - <a id="properties/payload/properties/method"></a>**`method`** *(object)*: The encryption method used to conceal the payload. Cannot contain additional properties.
    - <a id="properties/payload/properties/method/properties/name"></a>**`name`** *(string, required)*: The name of the encryption method.
    - <a id="properties/payload/properties/method/properties/args"></a>**`args`** *(array)*: Extra arguments to be provided to the method handler.
      - <a id="properties/payload/properties/method/properties/args/items"></a>**Items** *(string)*
- <a id="properties/signature"></a>**`signature`** *(string)*
