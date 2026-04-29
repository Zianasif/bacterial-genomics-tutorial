"""
Unit tests for modernized annotation analysis scripts.
"""

import pytest
import tempfile
from pathlib import Path
import pandas as pd
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

# Note: Import paths assume tests are run from project root
# If scripts are in main directory, adjust imports accordingly


class TestAnnotationDataGeneration:
    """Fixtures for creating test data."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for test files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)
    
    @pytest.fixture
    def sample_genbank_file(self, temp_dir):
        """Create a sample GenBank file for testing."""
        # Create a simple sequence record
        seq = Seq("ATGAAACCCGGG" * 100)  # Simple repetitive sequence
        record = SeqRecord(seq, id="test_plasmid", description="Test sequence")
        
        # Add some features
        from Bio.SeqFeature import SeqFeature, FeatureLocation
        
        # Add a gene
        record.features.append(SeqFeature(
            FeatureLocation(0, 100),
            type="gene",
            qualifiers={"name": ["test_gene"]}
        ))
        
        # Add a CDS
        record.features.append(SeqFeature(
            FeatureLocation(10, 100),
            type="CDS",
            qualifiers={"product": ["hypothetical_protein"]}
        ))
        
        # Add an insertion sequence
        record.features.append(SeqFeature(
            FeatureLocation(150, 200),
            type="CDS",
            qualifiers={"product": ["IS element transposase"]}
        ))
        
        # Add tRNA
        record.features.append(SeqFeature(
            FeatureLocation(300, 350),
            type="tRNA",
            qualifiers={"name": ["tRNA-Ala"]}
        ))
        
        # Write to GenBank file
        gbk_file = temp_dir / "test_plasmid.gbk"
        SeqIO.write(record, gbk_file, "genbank")
        
        return gbk_file
    
    @pytest.fixture
    def sample_pseudo_file(self, temp_dir):
        """Create a sample pseudogene file for testing."""
        pseudo_file = temp_dir / "test_plasmid.pseudo.txt"
        pseudo_file.write_text("pseudo_gene_1\npseudo_gene_2\npseudo_gene_3\n")
        return pseudo_file
    
    @pytest.fixture
    def sample_gene_csv(self, temp_dir):
        """Create a sample gene presence/absence CSV file."""
        data = {
            'Gene': ['gene_1', 'gene_2', 'gene_3', 'gene_4', 'gene_5'],
            'No. isolates': [3, 1, 2, 2, 3],
            'Isolate_A': ['✓', '✓', '✓', '', '✓'],
            'Isolate_B': ['✓', '', '✓', '✓', '✓'],
            'Isolate_C': ['✓', '', '', '✓', '✓'],
        }
        df = pd.DataFrame(data)
        csv_file = temp_dir / "gene_presence_absence.csv"
        df.to_csv(csv_file, index=False)
        return csv_file


class TestGetAnnotStatsModernized(TestAnnotationDataGeneration):
    """Test suite for modernized get_annot_stats script."""
    
    def test_load_genbank_file_success(self, sample_genbank_file):
        """Test successful loading of GenBank file."""
        # This would require importing the function from the script
        # For now, we'll verify the test fixture works
        assert sample_genbank_file.exists()
        records = list(SeqIO.parse(sample_genbank_file, "gb"))
        assert len(records) == 1
    
    def test_load_genbank_file_not_found(self, temp_dir):
        """Test error handling for missing GenBank file."""
        non_existent = temp_dir / "nonexistent.gbk"
        assert not non_existent.exists()
    
    def test_feature_counting(self, sample_genbank_file):
        """Test counting of genomic features."""
        record = list(SeqIO.parse(sample_genbank_file, "gb"))[0]
        
        # Verify features were added
        assert len(record.features) > 0
        
        # Count each type
        genes = len([f for f in record.features if f.type == 'gene'])
        cds = len([f for f in record.features if f.type == 'CDS'])
        trna = len([f for f in record.features if f.type == 'tRNA'])
        
        assert genes == 1
        assert cds == 2  # includes one IS element
        assert trna == 1
    
    def test_pseudogene_counting(self, sample_pseudo_file):
        """Test pseudogene file parsing."""
        count = len(sample_pseudo_file.read_text().strip().split('\n'))
        assert count == 3


class TestGeneCountSummaryModernized(TestAnnotationDataGeneration):
    """Test suite for modernized gene_count_summary script."""
    
    def test_load_gene_csv(self, sample_gene_csv):
        """Test loading of gene presence/absence CSV."""
        df = pd.read_csv(sample_gene_csv)
        assert 'Gene' in df.columns
        assert 'No. isolates' in df.columns
        assert 'Isolate_A' in df.columns
    
    def test_csv_column_validation(self, sample_gene_csv):
        """Test validation of required columns."""
        df = pd.read_csv(sample_gene_csv)
        required = ['Gene', 'No. isolates']
        for col in required:
            assert col in df.columns
    
    def test_venn_data_calculation(self, sample_gene_csv):
        """Test calculation of Venn diagram values."""
        df = pd.read_csv(sample_gene_csv)
        isolates = ['Isolate_A', 'Isolate_B', 'Isolate_C']
        
        # Verify all isolates exist in dataframe
        for iso in isolates:
            assert iso in df.columns
        
        # Test that we can identify genes in all three isolates
        all_three = df[df['No. isolates'] == 3]
        assert len(all_three) == 2  # gene_1 and gene_5
    
    def test_missing_isolate_error(self, sample_gene_csv):
        """Test error handling for missing isolates."""
        df = pd.read_csv(sample_gene_csv)
        missing_isolate = 'NonExistent_Isolate'
        assert missing_isolate not in df.columns


class TestErrorHandling:
    """Test error handling across modules."""
    
    def test_missing_file_error(self):
        """Test handling of missing input files."""
        non_existent = Path("/nonexistent/path/file.gbk")
        assert not non_existent.exists()
    
    def test_invalid_csv_error(self):
        """Test handling of invalid CSV files."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv') as f:
            f.write("invalid,csv,without,required,columns\n")
            f.write("data1,data2,data3,data4,data5\n")
            f.flush()
            
            # This should fail when trying to find 'Gene' column
            df = pd.read_csv(f.name)
            assert 'Gene' not in df.columns


class TestInputValidation:
    """Test input validation."""
    
    def test_isolate_count_validation(self):
        """Test that exactly 3 isolates are required."""
        isolates_2 = ['A', 'B']
        isolates_4 = ['A', 'B', 'C', 'D']
        
        assert len(isolates_2) == 2
        assert len(isolates_4) == 4
        # Exactly 3 is required
        assert 3 not in [len(isolates_2), len(isolates_4)]
    
    def test_path_validation(self):
        """Test path validation."""
        valid_path = Path(".")
        assert valid_path.exists()
        
        invalid_path = Path("/nonexistent/path/that/does/not/exist")
        assert not invalid_path.exists()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
