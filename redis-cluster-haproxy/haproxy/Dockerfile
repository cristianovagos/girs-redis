FROM haproxy:1.7

COPY entrypoint.sh /

RUN chmod +x /entrypoint.sh

EXPOSE 7010
EXPOSE 7020

ENTRYPOINT ["/entrypoint.sh"]

CMD ["haproxy", "-f", "/etc/haproxy/haproxy.cfg"]