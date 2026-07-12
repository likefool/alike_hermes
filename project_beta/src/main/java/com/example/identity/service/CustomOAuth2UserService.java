package com.example.identity.service;

import com.example.identity.model.User;
import com.example.identity.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.security.oauth2.core.user.DefaultOAuth2User;
import org.springframework.security.oauth2.core.user.OAuth2User;
import org.springframework.security.oauth2.user.OAuth2UserRequest;
import org.springframework.security.oauth2.user.OAuth2UserService;
import org.springframework.stereotype.Service;

import java.util.Map;
import java.util.Optional;

@Slf4j
@Service
@RequiredArgsConstructor
public class CustomOAuth2UserService implements OAuth2UserService<OAuth2UserRequest, OAuth2User> {

    private final UserRepository userRepository;

    @Override
    public OAuth2User loadUser(OAuth2UserRequest userRequest) {
        // Use the default implementation to fetch user info from the provider
        org.springframework.security.oauth2.client.userinfo.DefaultOAuth2UserService defaultUserService = 
            new org.springframework.security.oauth2.client.userinfo.DefaultOAuth2UserService();
        
        OAuth2User oAuth2User = defaultUserService.loadUser(userRequest);

        // Extract provider info
        String registrationId = userRequest.getClientRegistration().getRegistrationId().toUpperCase();
        
        // Extract unique identifier from provider (e.g., 'sub' in Google, 'id' in FB)
        // This is often implementation-specific, but 'sub' is common for OIDC
        String providerId = oAuth2User.getAttribute("sub");
        if (providerId == null) {
            providerId = oAuth2User.getAttribute("id");
        }

        String email = oAuth2User.getAttribute("email");
        String name = oAuth2User.getAttribute("name");

        log.info("Syncing social user: provider={} id={} email={}", registrationId, providerId, email);

        // Sync with local database
        User user = userRepository.findByProviderAndProviderId(registrationId, providerId)
                .orElseGet(() -> {
                    log.info("Creating new local user for social ID: {}", providerId);
                    return User.builder()
                            .username(email) // Using email as username for simplicity
                            .email(email)
                            .fullName(name)
                            .provider(registrationId)
                            .providerId(providerId)
                            .build();
                });

        // Update existing user info if necessary
        if (user.getId() == null) {
            user = userRepository.save(user);
        }

        // Return a decorated OAuth2User that includes our local User entity
        return new CustomOAuth2User(oAuth2User.getAttributes(), 
                                   oAuth2User.getAuthorities(), 
                                   user);
    }
}
