FROM driveone/onedrive:latest

COPY onedrive_entrypoint_addition.sh addition.sh

RUN sed -n '/echo "# Launching onedrive"/q;p' entrypoint.sh > myEntrypoint.sh
RUN cat addition.sh >> myEntrypoint.sh
RUN chmod a+x myEntrypoint.sh
RUN rm addition.sh

# ENTRYPOINT cat myEntrypoint.sh
ENTRYPOINT ./myEntrypoint.sh

# ENTRYPOINT ls -la /OneDrive/
