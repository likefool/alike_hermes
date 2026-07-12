# Project Beta: Identity & Access Management (IAM) Solution

A modern, secure, single-page identity solution built with **Spring Boot 3**, **OAuth2**, and **SQLite**. This project demonstrates a robust **Backend-for-Frontend (BFF)** pattern, where social identities (Google/Facebook) are synchronized with a local, persistent SQLite database.

## 🚀 Overview

The solution provides a seamless login flow:
1.  **Social Auth:** Users log in via Google or Facebook.
2.  **Identity Sync:** The application intercepts the OAuth2 response, extracts the unique provider ID, and synchronizes/creates a local user record in SQLite.
3.  **Session Management:** Uses secure, HTTP-only cookies to manage the user session on the frontend.
4.  **Dual-Layer Verification:** 
    *   **Session Layer (`/api/echo`):** Verifies the active security context.
    *   **Persistence Layer (`/api/user/profile`):** Verifies the local database synchronization.

## 🛠️ Tech Stack

*   **Backend:** Java 17+, Spring Boot 3.2.x, Spring Security, Spring Data JPA.
*   **Database:** SQLite (via JDBC & Hibernate Community Dialects).
*   **Frontend:** HTML5, JavaScript (ES6+), Tailwind CSS (BFF Pattern).
*   **Build Tool:** Maven.

## 📋 Prerequisites

*   **Java Development Kit (JDK) 17 or higher**
*   **Apache Maven**
*   **OAuth2 Credentials:** You will need valid `client-id` and `client-secret` from [Google Cloud Console](https://console.cloud.google.com/) or [Meta for Developers](https://developers.facebook.com/).

## ⚙️ Setup & Configuration

### 1. Configure Social Credentials
Open `src/main/resources/application.properties` and update the placeholders with your real credentials:

```properties
# Google Configuration
spring.security.oauth2.client.registration.google.client-id=YOUR_GOOGLE_CLIENT_ID
spring.security.oauth2.client.registration.google.client-secret=YOUR_GOOGLE_CLIENT_SECRET

# Facebook Configuration
spring.security.oauth2.client.registration.facebook.client-id=YOUR_FB_CLIENT_ID
spring.security.oauth2.client.registration.facebook.client-secret=YOUR_FB_CLIENT_SECRET
```

### 2. Build the Project
Run the following command in the project root:
```bash
mvn clean package
```

## 🏃 Running the Application

Once built, run the application using:
```bash
java -jar target/identity-solution-0.0.1-SNAPSHOT.jar
```

The server will start on `http://localhost:8080`.

## 🧪 Development & Testing

### Running Tests
To execute the full suite of security and integration tests:
```bash
mvn test
```

### Development Workflow
*   **Hot Reloading:** For active development, run using the Spring Boot Maven plugin:
    ```bash
    mvn spring-boot:run
    ```
*   **Database Inspection:** The SQLite database is located at `projects/project_beta/identity_db.db`. You can inspect it using any SQLite browser (e.g., DB Browser for SQLite).

## 🛡️ Security Design Notes

*   **BFF Pattern:** This project implements a Backend-for-Frontend architecture. The frontend does not handle sensitive OAuth2 tokens directly; instead, it interacts with the backend via secure, HTTP-only cookies.
*   **Identity Mapping:** The `CustomOAuth2UserService` ensures that even after the social session expires, the user's local identity remains intact and synchronized via the `providerId`.
*   **XSS/CSRF:** The frontend is built to be XSS-resistant, and the security configuration is designed to be hardened for production environments.
