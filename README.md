# Inference with LayoutLMv3 inside a Flask application

# To run the app, do the following steps:

1. Build the Docker image: `docker build -t flask-app .`

2. Run the Flask application inside the Docker container: `docker run -d -p 5000:5000 --name inference flask-app && docker logs -f inference`

3. Open your web browser and go to `http://localhost:5000/`

4. Upload your image and click on Upload to view teh results