from package import app
# import ssl



if __name__=="__main__":
    # context = ssl.SSLContext()
    # context.load_cert_chain('cert.crt', 'key.pem')
    # app.run(host="192.168.0.195",port=80, debug=True)
    app.run(debug=True)
