# Use an official OpenJDK runtime as a parent image
FROM openjdk:8-jre-alpine

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the JAR file and config.conf into the container at /usr/src/app
COPY target/scala-maven-0.1-SNAPSHOT-jar-with-dependencies.jar /usr/src/app
COPY config.conf /usr/src/app

# Run the application when the container launches
CMD ["java", "-cp", "scala-maven-0.1-SNAPSHOT-jar-with-dependencies.jar", "com.digikala.Kafka2Storage"]
