# Use Node.js 20 for WhatsApp bot
FROM node:20-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV NODE_ENV=production

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install --production

# Copy bot files
COPY whatsapp_bot_complete.js .
COPY config/ ./config/
COPY services/ ./services/
COPY views/ ./views/
COPY controllers/ ./controllers/

# Create directory for auth info
RUN mkdir -p /app/auth_info_baileys

# Create non-root user
RUN useradd -m -u 1000 botuser && \
  chown -R botuser:botuser /app
USER botuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD node -e "process.exit(0)"

# Run WhatsApp bot
CMD ["node", "whatsapp_bot_complete.js"]