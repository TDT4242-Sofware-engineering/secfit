# System and integration tests

### To run against production environment: 
Prerequisites:
- `npm install`
Then run:
- `npm run test-prod`

### To run within a test environment in docker-compose
- `./run.sh`
This will build backend, frontend and test image, then run the test on containers instantiated on these images.

### Consists of: 
jest puppeteer tests of all functionality including new functionality, and ensures that actions are properly handled and no new or existing functionality in the application is broken.