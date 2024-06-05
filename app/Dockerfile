
# Build the Go app
FROM golang:1.19 AS build
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN go build -o app .
ADD index.html.tmpl /
EXPOSE 80
CMD [ "/bin/sh", "-c", "/app/app http://db > /var/log/tns-app.log" ]
