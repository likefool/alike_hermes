package com.example.identity.controller;

import com.example.identity.model.User;
import com.example.identity.repository.UserRepository;
import com.example.identity.service.CustomOAuth2User;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.security.test.context.support.WithMockUser;
import org.springframework.test.web.servlet.MockMvc;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@SpringBootTest
@AutoConfigureMockMvc
class ApiSecurityTests {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private UserRepository userRepository;

    @Test
    void whenAccessingEchoWithoutAuth_thenReturnsUnauthenticated() throws Exception {
        mockMvc.perform(get("/api/echo"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.status").value("unauthenticated"));
    }

    @Test
    @WithMockUser(username = "testuser@example.com")
    void whenAccessingProfileWithMockUser_thenReturnsError() throws Exception {
        // Since we don't have a real OAuth2 user in this mock, 
        // it should fail to find the local profile in the DB.
        mockMvc.perform(get("/api/user/profile"))
                .andExpect(status().isNotFound())
                .andExpect(jsonPath("$.status").value("error"));
    }
}
