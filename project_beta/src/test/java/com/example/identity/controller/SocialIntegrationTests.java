package com.example.identity.controller;

import com.example.identity.model.User;
import com.example.identity.repository.UserRepository;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.security.test.web.servlet.request.SecurityMockMvcRequestPostProcessors;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.springframework.security.test.web.servlet.request.SecurityMockMvcRequestPostProcessors.oauth2Login;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@SpringBootTest
@AutoConfigureMockMvc
class SocialIntegrationTests {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private UserRepository userRepository;

    @Test
    void testSocialLoginSyncsWithLocalDatabase() throws Exception {
        // 1. Simulate a successful OAuth2 Login from a provider
        mockMvc.perform(MockMvcRequestBuilders.get("/api/user/profile")
                .with(oauth2Login()
                        .attributes(java.util.Map.of(
                                "sub", "google-12345",
                                "email", "tester@example.com",
                                "name", "Test User"
                        ))
                        .name("tester@example.com")
                ))
                // 2. The service should have created the user in SQLite
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.status").value("success"))
                .andExpect(jsonPath("$.local_username").value("tester@example.com"));

        // 3. Verify the user actually exists in the database
        var user = userRepository.findByUsername("tester@example.com");
        assertTrue(user.isPresent(), "User should be present in the database");
    }
}
