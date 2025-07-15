#!/usr/bin/env python3
"""
Script to update YAML files with better SEO-optimized titles and descriptions
"""

import yaml
import os

# SEO updates for each file
SEO_UPDATES = {
    'AI/ai-technical-writer.yaml': {
        'title': 'AI Technical Writing Software - Automated Documentation Creator',
        'description': 'Generate technical documentation with AI. Automate API docs, user guides & manuals. AI-powered technical writing platform for enterprise documentation teams.'
    },
    'AI/ai-agents.yaml': {
        'title': 'AI Documentation Agents - Intelligent Doc Assistants',
        'description': 'Deploy AI agents for documentation tasks. Automate content updates, answer queries & manage knowledge bases. Enterprise AI documentation assistant platform.'
    },
    'AI/custom-ai-content-prompts.yaml': {
        'title': 'Custom AI Documentation Prompts - Content Template Builder',
        'description': 'Create custom AI prompts for documentation. Build reusable content templates. Generate consistent technical docs with AI-powered prompt engineering.'
    },
    'AI/documentation-from-video.yaml': {
        'title': 'Video to Documentation Converter - AI Training Video Transcription',
        'description': 'Convert training videos to searchable docs instantly. AI-powered video documentation tool. Transform video content into structured knowledge base articles.'
    },
    'ai-documentation.yaml': {
        'title': 'AI Documentation Software - Intelligent Knowledge Base Platform',
        'description': 'Create AI-powered documentation automatically. Smart content generation, automated updates & intelligent search. Enterprise AI documentation management system.'
    },
    'api-documentation.yaml': {
        'title': 'API Documentation Tool - REST API Docs Generator',
        'description': 'Create beautiful API documentation. Interactive REST API docs with code examples. Developer-friendly API documentation platform for technical teams.'
    },
    'api-documentation-v2.yaml': {
        'title': 'API Documentation Platform - OpenAPI & Swagger Docs Builder',
        'description': 'Generate API docs from OpenAPI specs. Interactive API documentation with live testing. Modern API documentation tool for developers and technical writers.'
    },
    'content-management.yaml': {
        'title': 'Documentation CMS - Content Management for Knowledge Bases',
        'description': 'Manage documentation content efficiently. Version control, collaboration & publishing. Enterprise content management system for technical documentation.'
    },
    'customer-support.yaml': {
        'title': 'Customer Support Documentation - Self-Service Help Center',
        'description': 'Build self-service support docs. Reduce tickets 60% with searchable help articles. Customer support knowledge base software for enterprise help centers.'
    },
    'data_sheets.yaml': {
        'title': 'Product Data Sheet Software - Technical Spec Documentation',
        'description': 'Create professional data sheets online. Manage product specifications & technical details. Digital datasheet creator for product documentation teams.'
    },
    'doc_chatbots.yaml': {
        'title': 'Documentation Chatbot Platform - AI Help Bot Builder',
        'description': 'Build chatbots from your docs. Deploy intelligent help bots trained on knowledge bases. AI documentation chatbot software for automated support.'
    },
    'product-documentation.yaml': {
        'title': 'Product Documentation Software - User Guide & Manual Creator',
        'description': 'Create product docs users love. Build user guides, manuals & help content. Product documentation platform for SaaS and enterprise software teams.'
    },
    'quality-management.yaml': {
        'title': 'QMS Documentation Software - Quality Management System Docs',
        'description': 'Manage ISO & quality documentation. Compliance-ready QMS document control. Quality management documentation platform for regulated industries.'
    },
    'release-notes.yaml': {
        'title': 'Release Notes Tool - Changelog Management Software',
        'description': 'Create beautiful release notes. Manage product updates & changelogs. Automated release notes generator for software development teams.'
    },
    'sops.yaml': {
        'title': 'SOP Software - Standard Operating Procedure Management',
        'description': 'Create & manage SOPs online. Digital standard operating procedures with version control. SOP documentation platform for operations and compliance teams.'
    },
    'style-guide.yaml': {
        'title': 'Documentation Style Guide - Writing Standards Platform',
        'description': 'Build consistent documentation style guides. Manage writing standards & brand guidelines. Documentation style guide software for content teams.'
    },
    'technical-documentation.yaml': {
        'title': 'Technical Documentation Software - Technical Writing Platform',
        'description': 'Create professional technical docs. Manage complex documentation projects. Technical documentation tool for software developers and technical writers.'
    },
    'training-documentation.yaml': {
        'title': 'Training Documentation Platform - Employee Training Materials',
        'description': 'Create effective training docs. Build employee manuals & learning materials. Training documentation software for HR and L&D teams.'
    },
    'training-materials.yaml': {
        'title': 'Training Material Creator - Course Documentation Builder',
        'description': 'Design engaging training materials. Create course content & educational docs. Training material software for corporate learning and development.'
    },
    'user-manuals.yaml': {
        'title': 'User Manual Software - Online Instruction Manual Creator',
        'description': 'Create user manuals that users actually read. Build interactive instruction guides. User manual creator for product documentation teams.'
    },
    'industries.yaml': {
        'title': 'Industry Documentation Solutions - Sector-Specific Knowledge Bases',
        'description': 'Documentation platforms tailored for your industry. Compliance-ready solutions for regulated sectors. Enterprise documentation software by industry.'
    },
    'industries/compliance.yaml': {
        'title': 'Compliance Documentation Software - Regulatory Document Management',
        'description': 'Manage compliance docs efficiently. Audit-ready documentation for regulated industries. Compliance documentation platform with version control.'
    },
    'industries/energy.yaml': {
        'title': 'Energy Sector Documentation - Oil Gas & Utilities Doc Platform',
        'description': 'Documentation solutions for energy companies. Safety procedures, compliance docs & technical manuals. Energy industry documentation management system.'
    },
    'industries/government.yaml': {
        'title': 'Government Documentation Platform - Public Sector Doc Management',
        'description': 'Secure documentation for government agencies. Compliance-ready public sector knowledge base. Government documentation software with access controls.'
    },
    'industries/it-services.yaml': {
        'title': 'IT Documentation Software - MSP & Tech Services Platform',
        'description': 'Documentation tools for IT teams. Manage technical docs, runbooks & procedures. IT service documentation platform for MSPs and tech companies.'
    },
    'industries/manufacturing.yaml': {
        'title': 'Manufacturing Documentation - Production & Process Docs',
        'description': 'Digital documentation for manufacturers. Manage SOPs, work instructions & quality docs. Manufacturing documentation software for production teams.'
    },
    'industries/saas.yaml': {
        'title': 'SaaS Documentation Platform - Software Documentation Tools',
        'description': 'Documentation solutions for SaaS companies. API docs, user guides & knowledge bases. SaaS documentation software for product and support teams.'
    },
    'solutions.yaml': {
        'title': 'Documentation Solutions - Enterprise Knowledge Base Software',
        'description': 'Complete documentation solutions for every team. AI-powered platform for creating, managing & delivering docs. Enterprise documentation software suite.'
    }
}

def update_yaml_file(filepath, updates):
    """Update a YAML file with new title and description"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        if isinstance(data, list) and len(data) > 0:
            # Update the first item in the list
            data[0]['title'] = updates['title']
            data[0]['description'] = updates['description']
            
            # Write back to file
            with open(filepath, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
            
            print(f"✅ Updated: {os.path.basename(filepath)}")
            return True
        else:
            print(f"⚠️  Skipped: {os.path.basename(filepath)} - unexpected format")
            return False
            
    except Exception as e:
        print(f"❌ Error updating {filepath}: {str(e)}")
        return False

def main():
    """Main function to update all YAML files"""
    base_path = '/Users/philippetrounev/PycharmProjects/docsie-site/src/.data'
    
    updated = 0
    skipped = 0
    errors = 0
    
    print("Starting SEO updates for YAML files...\n")
    
    for relative_path, updates in SEO_UPDATES.items():
        full_path = os.path.join(base_path, relative_path)
        
        if os.path.exists(full_path):
            if update_yaml_file(full_path, updates):
                updated += 1
            else:
                errors += 1
        else:
            print(f"⚠️  File not found: {relative_path}")
            skipped += 1
    
    print(f"\n📊 Summary:")
    print(f"✅ Updated: {updated} files")
    print(f"⚠️  Skipped: {skipped} files")
    print(f"❌ Errors: {errors} files")

if __name__ == "__main__":
    main()