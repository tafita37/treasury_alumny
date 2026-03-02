INSERT INTO company_type (id, name) VALUES
(1, 'SARL'),
(2, 'SAS'),
(3, 'SA'),
(4, 'EURL'),
(5, 'Auto-entrepreneur');

INSERT INTO company (
    name,
    registration_number,
    tax_identification_number,
    email,
    phone,
    address,
    website_url,
    created_at,
    is_supplier,
    company_type_id
) VALUES
('Société Leroy Équipements', 'RCS-LE-001', 'TIN-LE-001', 'contact@leroy-equipements.fr', '+33 1 45 23 11 00', '12 Rue Industrielle, Paris', 'https://www.leroy-equipements.fr', '2015-03-12', TRUE, 3),

('Ateliers Dupont & Fils', 'RCS-DF-002', 'TIN-DF-002', 'contact@dupont-fils.fr', '+33 3 20 11 45 67', '8 Avenue des Artisans, Lille', 'https://www.dupont-fils.fr', '2012-07-25', TRUE, 1),

('Translog France', 'RCS-TL-003', 'TIN-TL-003', 'contact@translog.fr', '+33 4 72 33 21 90', '25 Zone Logistique, Lyon', 'https://www.translog.fr', '2018-01-10', TRUE, 2),

('Bureau Services Paris', 'RCS-BS-004', 'TIN-BS-004', 'contact@bsp.fr', '+33 1 55 66 77 88', '45 Rue de Bureau, Paris', 'https://www.bsp.fr', '2020-06-05', FALSE, 1),

('Électricité Martin SAS', 'RCS-EM-005', 'TIN-EM-005', 'contact@martin-elec.fr', '+33 5 56 44 22 11', '18 Rue Électrique, Bordeaux', 'https://www.martin-elec.fr', '2016-09-18', TRUE, 2),

('Nettoyage Pro Rhône', 'RCS-NP-006', 'TIN-NP-006', 'contact@nettoyage-rhone.fr', '+33 4 78 99 88 77', '3 Rue Propreté, Lyon', 'https://www.nettoyage-rhone.fr', '2019-11-30', TRUE, 1),

('Informatique Solutions France', 'RCS-IS-007', 'TIN-IS-007', 'contact@isf.fr', '+33 1 77 88 99 00', '22 Rue Numérique, Paris', 'https://www.isf.fr', '2017-04-22', FALSE, 2),

('Carburants Atlantique', 'RCS-CA-008', 'TIN-CA-008', 'contact@carburants-atl.fr', '+33 5 59 11 22 33', 'Port Atlantique, Nantes', 'https://www.carburants-atl.fr', '2014-02-14', TRUE, 3),

('Emballages Durables SAS', 'RCS-ED-009', 'TIN-ED-009', 'contact@emballages-durables.fr', '+33 2 40 55 66 77', '9 Rue Verte, Nantes', 'https://www.emballages-durables.fr', '2021-08-09', TRUE, 2),

('Maintenance Industrielle Nord', 'RCS-MI-010', 'TIN-MI-010', 'contact@maintenance-nord.fr', '+33 3 28 44 55 66', '60 Zone Industrielle, Lille', 'https://www.maintenance-nord.fr', '2013-12-01', TRUE, 3);