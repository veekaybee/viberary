# Model Store

This contains the API to Digital Ocean Spaces, an S3-Compatible Object storage with the embeddings for Viberary
and their ONNX representations.

API usage:

```
store = ModelStore(S3Client().conn())
store.upload_model()
store.download_model_dir("23-11-19-22")
store.get_model_metadata("23-11-19-22")
```
