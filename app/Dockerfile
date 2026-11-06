FROM alpine:3.9@sha256:414e0518bb9228d35e4cd5165567fb91d26c6a214e9c95899e1e056fcd349011
ADD app /
ADD index.html.tmpl /
EXPOSE 80
CMD [ "/bin/sh", "-c", "/app http://db > /var/log/tns-app.log" ]
