# syntax=docker/dockerfile:1
FROM rabbitmq
RUN rabbitmq-plugins enable rabbitmq_consistent_hash_exchange
RUN rabbitmq-plugins enable --offline rabbitmq_management
EXPOSE 15671 15672