/**
 * Company data types
 */

export interface Company {
  id: string;
  name: string;
  display_name: string;
  color: string;
  logo_url: string;
  tenets_file: string;
  description: string;
}

export interface CompaniesResponse {
  companies: Company[];
}
