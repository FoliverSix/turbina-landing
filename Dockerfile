FROM nginx:alpine

# Remove config padrão
RUN rm /etc/nginx/conf.d/default.conf

# Copia config do nginx
COPY nginx.conf /etc/nginx/conf.d/turbina.conf

# Copia os arquivos estáticos
COPY html/ /usr/share/nginx/html/

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
