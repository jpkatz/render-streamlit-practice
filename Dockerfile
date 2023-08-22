# Use an official Python runtime as a parent image
# FROM python:3.10.12

# # Set the working directory to /app
# WORKDIR /app

# # Copy the current directory contents into the container at /app
# COPY . /app

# # Install any needed packages specified in requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt

# # Make port 80 available to the world outside this container
# EXPOSE 80

# RUN mkdir ~/.streamlit
# RUN cp .streamlit/config.prod.toml ~/.streamlit/config.toml
# RUN cp .streamlit/credentials.prod.toml ~/.streamlit/credentials.toml

# ENTRYPOINT [ "/bin/bash", "./scripts/run_streamlit_app.sh"]

FROM python:3.10.12
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
CMD streamlit run app.py
