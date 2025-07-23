# Andy Grails' Website

This is the main repository for the **Andy Grails** website — a personal project
to showcase and stream music under the nickname *Andy Grails*. The site is 
powered by a **Java backend** and an **Angular frontend**, structured as 
Git submodules.

## Repository Structure

This repository acts as a wrapper for the two core components:

andy.grails/
- andy.grails.backend/   (Java Spring Boot backend: API, data services)
- andy.grails.frontend/  (Angular frontend: UI and client logic)

### Submodules

- [**backend**](https://github.com/aistomin/andy.grails.backend):  
  A Java Spring Boot application providing RESTful APIs to serve music data, 
  media, and metadata.

- [**frontend**](https://github.com/aistomin/andy.grails.frontend):  
  An Angular-based web application that presents the user interface, consumes
  the backend API, and delivers the overall user experience.

## Getting Started

To clone this repository including its submodules:

```bash
git clone --recurse-submodules git@github.com:aistomin/andy.grails.git
```

If you've already cloned the repository without submodules, run:

```bash
git submodule update --init --recursive
```

Each submodule has its own `README.md` with specific instructions for building
and running the backend and frontend.
