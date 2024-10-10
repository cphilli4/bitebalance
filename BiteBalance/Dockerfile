# Use Node.js 18 as the base image
FROM node:18


# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json first
COPY package.json package-lock.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application files to the working directory
COPY . .

# Expose the necessary ports for the Expo server
EXPOSE 19000 19001 19002

# Start the Expo development server using npx
CMD ["npx", "expo", "start", "--tunnel"]
