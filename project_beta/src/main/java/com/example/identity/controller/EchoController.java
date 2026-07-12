package com.example.identity.controller;

import com.example.identity.model.User;
import com.example.identity.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.security.oauth2.core.user.OAuth2User;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/api")
public class EchoController {

    @GetMapping("/echo")
    public ResponseEntity<Map<String, Object>> echo(Authentication authentication) {
        Map<String, Object> response = new HashMap<>();
        
        if (authentication == null) {
            response.put("status", "unauthenticated");
            return ResponseEntity.ok(response);
        }

        response.put("status", "authenticated");
        response.put("principal", authentication.getName());
        response.put("authorities", authentication.getAuthorities());

        if (authentication.getPrincipal() instanceof OAuth2User) {
            OAuth2User oauth2User = (OAuth2User) authentication.getPrincipal();
            response.put("attributes", oauth2User.getAttributes());
        }

        return ResponseEntity.ok(response);
    }
}
