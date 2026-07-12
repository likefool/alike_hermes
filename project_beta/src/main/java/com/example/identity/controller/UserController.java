package com.example.identity.controller;

import com.example.identity.model.User;
import com.example.identity.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.security.oauth2.core.user.OAuth2User;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/api/user")
@RequiredArgsConstructor
public class UserController {

    private final UserRepository userRepository;

    @GetMapping("/profile")
    public ResponseEntity<Map<String, Object>> getLocalProfile(@AuthenticationPrincipal OAuth2User oauth2User) {
        Map<String, Object> response = new HashMap<>();
        
        // The 'name' in our CustomOAuth2User is the username (email)
        String username = oauth2User.getName();

        // Find the user in our local SQLite DB
        var userOptional = userRepository.findByUsername(username);

        if (userOptional.isEmpty()) {
            response.put("status", "error");
            response.put("message", "Local user profile not found.");
            return ResponseEntity.status(404).body(response);
        }

        User localUser = userOptional.get();
        
        response.put("status", "success");
        response.put("local_id", localUser.getId());
        response.put("local_username", localUser.getUsername());
        response.put("local_email", localUser.getEmail());
        response.put("local_fullName", localUser.getFullName());
        response.put dapat (localUser.getProvider());
        response.put("local_provider", localUser.getProvider());
        response.put("created_at", localUser.getCreatedAt().toString());

        return ResponseEntity.ok(response);
    }
}
