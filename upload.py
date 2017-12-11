curl -X POST \
  http://localhost:3001/upload/COMPSCI311/lecture-zip \
  -H 'cache-control: no-cache' \
  -H 'content-type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW' \
  -H 'postman-token: d02cc18e-b597-ecf4-f3d5-b5f02a055628' \
  -F file=@CompTEST2.zip
