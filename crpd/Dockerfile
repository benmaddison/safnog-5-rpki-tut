FROM crpd:latest

# add bootstrap script
COPY bootstrap /etc/init.d/
RUN chmod +x /etc/init.d/bootstrap
# run bootstrap on startup
RUN echo '/etc/init.d/bootstrap' >> /etc/init.d/rcS
